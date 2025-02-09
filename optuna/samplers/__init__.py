import optuna
from optuna.samplers.base import BaseSampler  # NOQA
from optuna.samplers.random import RandomSampler  # NOQA
from optuna.samplers.tpe import TPESampler  # NOQA

if optuna.types.TYPE_CHECKING:
    from typing import Dict  # NOQA

    from optuna.distributions import BaseDistribution  # NOQA
    from optuna.study import BaseStudy  # NOQA


def product_search_space(study):
    # type: (BaseStudy) -> Dict[str, BaseDistribution]
    """Return the product search space of the :class:`~optuna.study.BaseStudy`.

    Product search space contains the product set of parameter distributions that have been
    suggested in the completed trials of the study so far.
    If there are multiple parameters that have the same name but different distributions,
    neither is included in the resulting search space
    (i.e., the parameters with dynamic value ranges are excluded).

    Returns:
        A dictionary containing the parameter names and parameter's distributions.
    """

    search_space = None
    for trial in study.trials:
        if trial.state != optuna.structs.TrialState.COMPLETE:
            continue

        if search_space is None:
            search_space = trial.distributions
            continue

        delete_list = []
        for param_name, param_distribution in search_space.items():
            if param_name not in trial.distributions:
                delete_list.append(param_name)
            elif trial.distributions[param_name] != param_distribution:
                delete_list.append(param_name)

        for param_name in delete_list:
            del search_space[param_name]

    return search_space or {}
