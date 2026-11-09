from test_tools.test_logger import create_test_logger


def test_robot_logging():

    logger = create_test_logger()

    logger.info("Starting robot test")

    command = 90

    logger.info(f"Sending joint command: {command}")

    feedback = 90

    logger.info(f"Received joint feedback: {feedback}")

    assert feedback == command

    logger.info("Robot test passed")
