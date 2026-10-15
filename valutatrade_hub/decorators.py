"""Декораторы."""

import functools
import logging


def log_action(action, verbose=False):
    """Логирует операции покупки и продажи."""

    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, currency_code, amount):
            logger = logging.getLogger("valutatrade")
            info = (
                f"{action} user='{user.username}' currency='{currency_code}' "
                f"amount={amount:.4f}"
            )
            try:
                result = func(user, currency_code, amount)
            except Exception as e:
                logger.info(
                    f"{info} result=ERROR error_type={type(e).__name__} "
                    f"error_message='{e}'"
                )
                raise
            rate, old_balance, new_balance, total = result
            message = f"{info} rate={rate:.2f} base='USD' result=OK"
            if verbose:
                message += f" balance={old_balance:.4f}->{new_balance:.4f}"
            logger.info(message)
            return result

        return wrapper

    return decorator