import uuid

from ariadne import convert_kwargs_to_snake_case
from celery import current_app
from celery.result import AsyncResult
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from strategy.models import Strategy, StrategySharing, UserStrategy


# Queries
@convert_kwargs_to_snake_case
def get_user_strategy(*_, strategy_id):
    try:
        strategy = UserStrategy.objects.get(strategy=strategy_id)

        return {
            "strategy_id": strategy_id,
            "strategy_name": strategy.strategy_name,
            "created_at": strategy.created_at,
            "updated_at": strategy.updated_at,
        }
    except UserStrategy.DoesNotExist:
        raise Exception("This strategy ID does not exist")


def get_strategy(_, info, strategyId, commitId=None):
    try:
        user_strategy = UserStrategy.objects.filter(
            strategy=strategyId, user=info.context["user"]
        )
        strategy_sharing = StrategySharing.objects.filter(
            strategy__strategy=strategyId, user=info.context["user"]
        )

        if user_strategy.exists() or strategy_sharing.exists():
            if user_strategy.exists():
                user_strategy = user_strategy[0]

            if strategy_sharing.exists():
                strategy_sharing = strategy_sharing[0]

            strategy = None
            if commitId:
                strategy = Strategy.objects.get(
                    strategy=user_strategy,
                    commit=commitId,
                )

            else:
                strategy = (
                    Strategy.objects.filter(
                        strategy__strategy=strategyId,
                    )
                    .order_by("-updated_at")
                    .first()
                )

            return {
                "strategy": {
                    "strategy_id": strategyId,
                    "strategy_name": user_strategy.strategy_name,
                    "created_at": user_strategy.created_at,
                    "updated_at": user_strategy.updated_at,
                },
                "commit_id": str(strategy.commit),
                "flow_metadata": strategy.flow_metadata,
                "input": strategy.input,
                "output": strategy.output,
                "created_at": strategy.created_at,
                "updated_at": strategy.updated_at,
            }
        else:
            raise Exception("You are not authorized to view this strategy")
    except Strategy.DoesNotExist:
        raise Exception("The strategy and commit pair does not exist")


@convert_kwargs_to_snake_case
def list_user_strategies(_, info):
    return [
        {
            "strategy_id": user_strategy.strategy,
            "strategy_name": user_strategy.strategy_name,
            "created_at": user_strategy.created_at,
            "updated_at": user_strategy.updated_at,
        }
        for user_strategy in UserStrategy.objects.filter(user=info.context["user"])
    ]


@convert_kwargs_to_snake_case
def list_strategies(_, info):
    return [
        {
            "strategy": strategy.strategy,
            "commit_id": strategy.commit,
            "flow_metadata": strategy.flow_metadata,
            "input": strategy.input,
            "output": strategy.output,
            "created_at": strategy.created_at,
            "updated_at": strategy.updated_at,
        }
        for strategy in Strategy.objects.filter(strategy__user=info.context["user"])
    ]


@convert_kwargs_to_snake_case
def list_shared_users(*_, strategy_id):
    return [
        {
            "email": sharing_permission.user.email,
            "permissions": sharing_permission.permissions,
        }
        for sharing_permission in StrategySharing.objects.filter(
            strategy__strategy=strategy_id
        )
    ]


def get_task_result(*_, taskId):
    task = AsyncResult(taskId)
    if not task.status == "SUCCESS":
        return {
            "status": task.status,
            "output": None,
        }

    return {
        "status": task.status,
        "output": task.get(),
    }


# Mutations
@convert_kwargs_to_snake_case
def create_user_strategy(_, info, strategy_name):
    try:
        strategy_id = uuid.uuid4()

        user_strategy = UserStrategy.objects.create(
            strategy=strategy_id, user=info.context["user"], strategy_name=strategy_name
        )

        return {
            "strategy_id": strategy_id,
            "strategy_name": user_strategy.strategy_name,
            "created_at": user_strategy.created_at,
            "updated_at": user_strategy.updated_at,
        }
    except IntegrityError:
        raise Exception("The strategy ID - user pair already exists")
    except Exception:
        raise Exception("There was an unhandled error creating the user strategy")


def create_strategy(_, info, strategyId, metadata, inputs, outputs, commitId=None):
    try:
        try:
            uuid.UUID(strategyId, version=4)
        except ValueError:
            raise Exception("The strategy id is invalid")

        try:
            if commitId:
                uuid.UUID(commitId, version=4)
        except ValueError:
            raise Exception("The commit id is invalid")

        user_strategy = UserStrategy.objects.filter(
            strategy=strategyId, user=info.context["user"]
        )
        strategy_sharing = StrategySharing.objects.filter(
            strategy__strategy=strategyId, user=info.context["user"]
        )

        if not user_strategy.exists() and not strategy_sharing.exists():
            raise Exception("This strategy does not exist")

        strategy = None
        if user_strategy.exists():
            strategy = user_strategy.first()

        if strategy_sharing.exists():
            if strategy_sharing.first().permissions == 1:
                raise Exception("You only have read permissions on this strategy")

            strategy = strategy_sharing.first().strategy

        # If commitId is None, then generates a new one. Otherwise uses the one passed in
        commit_id = commitId
        if not commitId:
            commit_id = uuid.uuid4()

        Strategy.objects.create(
            strategy=strategy,
            commit=commit_id,
            flow_metadata=metadata,
            input=inputs,
            output=outputs,
        )

        return True
    except IntegrityError:
        raise Exception("The strategy-commit pair already exist")
    except ValidationError:
        raise Exception("There was a validation error")


@convert_kwargs_to_snake_case
def delete_strategy(_, info, strategy_id):
    try:
        UserStrategy.objects.get(
            user=info.context["user"], strategy=strategy_id
        ).delete()
        return True
    except UserStrategy.DoesNotExist:
        raise Exception("Strategy does not exist")
    except Exception:
        raise Exception("An unhandled error occurred when deleting this strategy")


def dispatch_run_strategy(*_, nodeList, edgeList, strategyType):
    if strategyType == "SCREENER":
        task = current_app.send_task(
            "strategy.tasks.run_screener",
            queue="screener",
            routing_key="screener_task",
            args=(nodeList, edgeList),
        )
        return {"status": True, "task_id": task.task_id}
    elif strategyType == "BACKTEST":
        task = current_app.send_task(
            "strategy.tasks.run_strategy",
            queue="backtest",
            routing_key="backtest_task",
            args=(nodeList, edgeList),
        )
        return {"status": True, "task_id": task.task_id}
    else:
        return {"status": False, "task_id": None}


@convert_kwargs_to_snake_case
def share_strategy(*_, strategy_id, email, permissions):
    user_strategy = UserStrategy.objects.get(strategy=strategy_id)
    user = User.objects.get(email=email)

    StrategySharing.objects.update_or_create(
        strategy=user_strategy, user=user, permissions=permissions
    )

    return {"shared": True}
