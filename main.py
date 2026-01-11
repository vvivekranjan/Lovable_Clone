import argparse
import sys
import traceback
import logging

from Agent.graph import agent

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

    args = parser.parse_args()

    try:
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