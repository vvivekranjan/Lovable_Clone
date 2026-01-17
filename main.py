import argparse
import sys
import traceback
import logging

from Agent.graph import agent
from Agent.config import is_configured, load_config, update_api_config, get_api_provider, get_model_name

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def validate_recursion_limit(value: int) -> int:
    """Validate that the recursion limit is reasonable.
    
    Args:
        value: The recursion limit value
        
    Returns:
        The validated recursion limit
        
    Raises:
        argparse.ArgumentTypeError: If the value is invalid
    """
    try:
        int_value = int(value)
        if int_value <= 0:
            raise argparse.ArgumentTypeError("Recursion limit must be positive")
        if int_value > 1000:
            raise argparse.ArgumentTypeError("Recursion limit too high (max: 1000)")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid recursion limit: {value}")


def setup_api_configuration():
    """Setup API configuration if not already configured."""
    if is_configured():
        # Show current configuration
        config = load_config()
        logger.info(f"Using API Provider: {config['api_provider']}")
        logger.info(f"Model: {config['model_name']}")
        return
    
    print("\n" + "="*60)
    print("🤖 API Configuration Setup")
    print("="*60)
    print("Welcome! Please configure your AI API settings.\n")
    
    # API Provider selection
    providers = ["google", "openai", "anthropic"]
    print("Available providers:")
    for i, provider in enumerate(providers, 1):
        print(f"  {i}. {provider}")
    
    while True:
        try:
            choice = int(input("\nSelect provider (1-3): "))
            if 1 <= choice <= 3:
                api_provider = providers[choice - 1]
                break
            print("Invalid choice. Please enter 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")
    
    # API Key input
    print(f"\nYou selected: {api_provider}")
    if api_provider == "google":
        print("Get your API key: https://makersuite.google.com/app/apikey")
    elif api_provider == "openai":
        print("Get your API key: https://platform.openai.com/account/api-keys")
    elif api_provider == "anthropic":
        print("Get your API key: https://console.anthropic.com/")
    
    api_key = input(f"\nEnter your {api_provider} API key: ").strip()
    if not api_key:
        print("Error: API key cannot be empty")
        sys.exit(1)
    
    # Model name input
    model_suggestions = {
        "google": "gemini-2.5-flash",
        "openai": "gpt-4",
        "anthropic": "claude-3-5-sonnet-20241022"
    }
    default_model = model_suggestions.get(api_provider)
    
    model_name = input(f"\nEnter model name (default: {default_model}): ").strip()
    if not model_name:
        model_name = default_model
    
    # Save configuration
    try:
        update_api_config(api_provider, api_key, model_name)
        print(f"\n✅ Configuration saved successfully!")
        print(f"Provider: {api_provider}")
        print(f"Model: {model_name}")
        print("="*60 + "\n")
        logger.info(f"API configured with {api_provider} - {model_name}")
    except Exception as e:
        print(f"❌ Error saving configuration: {e}")
        sys.exit(1)


def main():
    """Main entry point for the project planner agent."""
    parser = argparse.ArgumentParser(
        description="Run engineering project planner",
        epilog="Example: python main.py --recursion-limit 100"
    )
    parser.add_argument(
        "--recursion-limit", "-r",
        type=validate_recursion_limit,
        default=100,
        help="Recursion limit for processing (default: 100, max: 1000)"
    )
    parser.add_argument(
        "--setup-api",
        action="store_true",
        help="Setup or change API configuration"
    )

    args = parser.parse_args()

    try:
        # Setup API if requested or not configured
        if args.setup_api or not is_configured():
            setup_api_configuration()
        
        user_prompt = input("What would you like to build: ").strip()
        
        if not user_prompt:
            logger.error("User prompt cannot be empty")
            print("Error: Please provide a description of what you want to build.")
            sys.exit(1)
        
        logger.info(f"Processing user prompt: {user_prompt[:50]}...")
        result = agent.invoke(
            {"user_prompt": user_prompt},
            {"recursion_limit": args.recursion_limit}
        )
        logger.info("Project generation completed successfully")
        print("\nFinal State:", result)
        
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user.")
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        traceback.print_exc()
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()