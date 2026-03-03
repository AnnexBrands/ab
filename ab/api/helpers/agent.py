"""Agent assignment helpers — change origin/delivery agent by code.

Provides convenience methods for reassigning job agents using friendly
company codes (e.g., ``"3P-5153"``) instead of raw UUIDs.  Code-to-UUID
resolution uses the existing :class:`~ab.cache.CodeResolver`.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from ab.api.models.enums import ServiceType

if TYPE_CHECKING:
    from ab.api.endpoints.jobs import JobsEndpoint
    from ab.cache import CodeResolver


class AgentHelpers:
    """High-level agent assignment operations with code resolution.

    Usage::

        api = ABConnectAPI()
        api.jobs.agent.oa(12345, "3P-5153")
        api.jobs.agent.da(12345, "9999AZ", recalculate_price=True)
    """

    def __init__(self, jobs: JobsEndpoint, resolver: CodeResolver) -> None:
        self._jobs = jobs
        self._resolver = resolver

    def change(
        self,
        job: int | str,
        agent: str,
        *,
        service_type: Union[ServiceType, int],
        recalculate_price: bool = False,
        apply_rebate: bool = False,
    ) -> Any:
        """Change the agent for a job.

        Args:
            job: Job display ID.
            agent: Agent company code (e.g. ``"3P-5153"``) or UUID.
                Codes are resolved via the cache service automatically.
            service_type: Agent service type — accepts a
                :class:`~ab.api.models.enums.ServiceType` enum or raw ``int``.
            recalculate_price: Recalculate job price after the change.
            apply_rebate: Apply rebate after the change.

        Returns:
            :class:`~ab.api.models.shared.ServiceBaseResponse`
        """
        resolved = self._resolver.resolve(agent)
        return self._jobs.change_agent(
            int(job),
            data={
                "serviceType": int(service_type),
                "agentId": resolved,
                "recalculatePrice": recalculate_price,
                "applyRebate": apply_rebate,
            },
        )

    def oa(
        self,
        job: int | str,
        agent: str,
        *,
        recalculate_price: bool = False,
        apply_rebate: bool = False,
    ) -> Any:
        """Change the origin agent (pick-and-pack).

        Shortcut for ``change(job, agent, service_type=ServiceType.PICKANDPACK)``.

        Args:
            job: Job display ID.
            agent: Agent company code or UUID.
            recalculate_price: Recalculate job price after the change.
            apply_rebate: Apply rebate after the change.

        Returns:
            :class:`~ab.api.models.shared.ServiceBaseResponse`
        """
        return self.change(
            job, agent,
            service_type=ServiceType.PICKANDPACK,
            recalculate_price=recalculate_price,
            apply_rebate=apply_rebate,
        )

    def da(
        self,
        job: int | str,
        agent: str,
        *,
        recalculate_price: bool = False,
        apply_rebate: bool = False,
    ) -> Any:
        """Change the delivery agent.

        Shortcut for ``change(job, agent, service_type=ServiceType.DELIVERY)``.

        Args:
            job: Job display ID.
            agent: Agent company code or UUID.
            recalculate_price: Recalculate job price after the change.
            apply_rebate: Apply rebate after the change.

        Returns:
            :class:`~ab.api.models.shared.ServiceBaseResponse`
        """
        return self.change(
            job, agent,
            service_type=ServiceType.DELIVERY,
            recalculate_price=recalculate_price,
            apply_rebate=apply_rebate,
        )
