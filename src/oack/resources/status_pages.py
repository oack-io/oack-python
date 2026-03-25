"""Status page resource."""

from __future__ import annotations

import json
from typing import TYPE_CHECKING

from oack.types.status_pages import (
    Component,
    ComponentGroup,
    Incident,
    IncidentTemplate,
    IncidentUpdate,
    Maintenance,
    MaintenanceUpdate,
    StatusPage,
    Subscriber,
    Watchdog,
)

if TYPE_CHECKING:
    from oack._client import AsyncBaseClient, BaseClient


def _page_path(account_id: str, page_id: str) -> str:
    return f"/api/v1/accounts/{account_id}/status-pages/{page_id}"


class AsyncStatusPages:
    def __init__(self, client: AsyncBaseClient) -> None:
        self._client = client

    # --- Status pages ---

    async def create(self, account_id: str, params: dict) -> StatusPage:
        resp = await self._client.request("POST", f"/api/v1/accounts/{account_id}/status-pages", json=params)
        return StatusPage.model_validate_json(resp)

    async def list(self, account_id: str) -> list[StatusPage]:
        resp = await self._client.request("GET", f"/api/v1/accounts/{account_id}/status-pages")
        return [StatusPage.model_validate(p) for p in json.loads(resp)]

    async def get(self, account_id: str, page_id: str) -> StatusPage:
        resp = await self._client.request("GET", _page_path(account_id, page_id))
        return StatusPage.model_validate_json(resp)

    async def update(self, account_id: str, page_id: str, params: dict) -> StatusPage:
        resp = await self._client.request("PUT", _page_path(account_id, page_id), json=params)
        return StatusPage.model_validate_json(resp)

    async def delete(self, account_id: str, page_id: str) -> None:
        await self._client.request("DELETE", _page_path(account_id, page_id))

    # --- Component groups ---

    async def create_component_group(self, account_id: str, page_id: str, params: dict) -> ComponentGroup:
        resp = await self._client.request("POST", _page_path(account_id, page_id) + "/component-groups", json=params)
        return ComponentGroup.model_validate_json(resp)

    async def list_component_groups(self, account_id: str, page_id: str) -> list[ComponentGroup]:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + "/component-groups")
        return [ComponentGroup.model_validate(g) for g in json.loads(resp)]

    async def get_component_group(self, account_id: str, page_id: str, group_id: str) -> ComponentGroup:
        groups = await self.list_component_groups(account_id, page_id)
        for g in groups:
            if g.id == group_id:
                return g
        from oack._exceptions import NotFoundError

        raise NotFoundError("component group not found")

    async def update_component_group(
        self, account_id: str, page_id: str, group_id: str, params: dict
    ) -> ComponentGroup:
        resp = await self._client.request(
            "PUT",
            _page_path(account_id, page_id) + f"/component-groups/{group_id}",
            json=params,
        )
        return ComponentGroup.model_validate_json(resp)

    async def delete_component_group(self, account_id: str, page_id: str, group_id: str) -> None:
        await self._client.request("DELETE", _page_path(account_id, page_id) + f"/component-groups/{group_id}")

    # --- Components ---

    async def create_component(self, account_id: str, page_id: str, params: dict) -> Component:
        resp = await self._client.request("POST", _page_path(account_id, page_id) + "/components", json=params)
        return Component.model_validate_json(resp)

    async def list_components(self, account_id: str, page_id: str) -> list[Component]:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + "/components")
        return [Component.model_validate(c) for c in json.loads(resp)]

    async def get_component(self, account_id: str, page_id: str, comp_id: str) -> Component:
        components = await self.list_components(account_id, page_id)
        for c in components:
            if c.id == comp_id:
                return c
        from oack._exceptions import NotFoundError

        raise NotFoundError("component not found")

    async def update_component(self, account_id: str, page_id: str, comp_id: str, params: dict) -> Component:
        resp = await self._client.request(
            "PUT", _page_path(account_id, page_id) + f"/components/{comp_id}", json=params
        )
        return Component.model_validate_json(resp)

    async def delete_component(self, account_id: str, page_id: str, comp_id: str) -> None:
        await self._client.request("DELETE", _page_path(account_id, page_id) + f"/components/{comp_id}")

    # --- Incidents ---

    async def create_incident(self, account_id: str, page_id: str, params: dict) -> Incident:
        resp = await self._client.request("POST", _page_path(account_id, page_id) + "/incidents", json=params)
        return Incident.model_validate_json(resp)

    async def list_incidents(self, account_id: str, page_id: str) -> list[Incident]:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + "/incidents")
        return [Incident.model_validate(i) for i in json.loads(resp)]

    async def get_incident(self, account_id: str, page_id: str, incident_id: str) -> Incident:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + f"/incidents/{incident_id}")
        return Incident.model_validate_json(resp)

    async def update_incident(self, account_id: str, page_id: str, incident_id: str, params: dict) -> Incident:
        resp = await self._client.request(
            "PUT", _page_path(account_id, page_id) + f"/incidents/{incident_id}", json=params
        )
        return Incident.model_validate_json(resp)

    async def delete_incident(self, account_id: str, page_id: str, incident_id: str) -> None:
        await self._client.request("DELETE", _page_path(account_id, page_id) + f"/incidents/{incident_id}")

    async def post_incident_update(
        self, account_id: str, page_id: str, incident_id: str, message: str, status: str
    ) -> IncidentUpdate:
        resp = await self._client.request(
            "POST",
            _page_path(account_id, page_id) + f"/incidents/{incident_id}/updates",
            json={"body": message, "status": status},
        )
        return IncidentUpdate.model_validate_json(resp)

    # --- Maintenances ---

    async def create_maintenance(self, account_id: str, page_id: str, params: dict) -> Maintenance:
        resp = await self._client.request("POST", _page_path(account_id, page_id) + "/maintenances", json=params)
        return Maintenance.model_validate_json(resp)

    async def list_maintenances(self, account_id: str, page_id: str) -> list[Maintenance]:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + "/maintenances")
        return [Maintenance.model_validate(m) for m in json.loads(resp)]

    async def get_maintenance(self, account_id: str, page_id: str, maint_id: str) -> Maintenance:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + f"/maintenances/{maint_id}")
        return Maintenance.model_validate_json(resp)

    async def update_maintenance(self, account_id: str, page_id: str, maint_id: str, params: dict) -> Maintenance:
        resp = await self._client.request(
            "PUT", _page_path(account_id, page_id) + f"/maintenances/{maint_id}", json=params
        )
        return Maintenance.model_validate_json(resp)

    async def delete_maintenance(self, account_id: str, page_id: str, maint_id: str) -> None:
        await self._client.request("DELETE", _page_path(account_id, page_id) + f"/maintenances/{maint_id}")

    async def post_maintenance_update(
        self, account_id: str, page_id: str, maint_id: str, message: str, status: str
    ) -> MaintenanceUpdate:
        resp = await self._client.request(
            "POST",
            _page_path(account_id, page_id) + f"/maintenances/{maint_id}/updates",
            json={"body": message, "status": status},
        )
        return MaintenanceUpdate.model_validate_json(resp)

    # --- Subscribers ---

    async def list_subscribers(self, account_id: str, page_id: str) -> list[Subscriber]:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + "/subscribers")
        return [Subscriber.model_validate(s) for s in json.loads(resp)]

    async def remove_subscriber(self, account_id: str, page_id: str, subscriber_id: str) -> None:
        await self._client.request("DELETE", _page_path(account_id, page_id) + f"/subscribers/{subscriber_id}")

    # --- Incident templates ---

    async def create_incident_template(self, account_id: str, page_id: str, params: dict) -> IncidentTemplate:
        resp = await self._client.request("POST", _page_path(account_id, page_id) + "/incident-templates", json=params)
        return IncidentTemplate.model_validate_json(resp)

    async def list_incident_templates(self, account_id: str, page_id: str) -> list[IncidentTemplate]:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + "/incident-templates")
        return [IncidentTemplate.model_validate(t) for t in json.loads(resp)]

    async def update_incident_template(
        self, account_id: str, page_id: str, template_id: str, params: dict
    ) -> IncidentTemplate:
        resp = await self._client.request(
            "PUT",
            _page_path(account_id, page_id) + f"/incident-templates/{template_id}",
            json=params,
        )
        return IncidentTemplate.model_validate_json(resp)

    async def delete_incident_template(self, account_id: str, page_id: str, template_id: str) -> None:
        await self._client.request("DELETE", _page_path(account_id, page_id) + f"/incident-templates/{template_id}")

    # --- Watchdogs ---

    async def create_watchdog(self, account_id: str, page_id: str, comp_id: str, params: dict) -> Watchdog:
        resp = await self._client.request(
            "POST", _page_path(account_id, page_id) + f"/components/{comp_id}/watchdogs", json=params
        )
        return Watchdog.model_validate_json(resp)

    async def list_watchdogs(self, account_id: str, page_id: str, comp_id: str) -> list[Watchdog]:
        resp = await self._client.request("GET", _page_path(account_id, page_id) + f"/components/{comp_id}/watchdogs")
        return [Watchdog.model_validate(w) for w in json.loads(resp)]

    async def delete_watchdog(self, account_id: str, page_id: str, comp_id: str, watchdog_id: str) -> None:
        await self._client.request(
            "DELETE", _page_path(account_id, page_id) + f"/components/{comp_id}/watchdogs/{watchdog_id}"
        )


class StatusPages:
    def __init__(self, client: BaseClient) -> None:
        self._client = client

    # --- Status pages ---

    def create(self, account_id: str, params: dict) -> StatusPage:
        resp = self._client.request("POST", f"/api/v1/accounts/{account_id}/status-pages", json=params)
        return StatusPage.model_validate_json(resp)

    def list(self, account_id: str) -> list[StatusPage]:
        resp = self._client.request("GET", f"/api/v1/accounts/{account_id}/status-pages")
        return [StatusPage.model_validate(p) for p in json.loads(resp)]

    def get(self, account_id: str, page_id: str) -> StatusPage:
        resp = self._client.request("GET", _page_path(account_id, page_id))
        return StatusPage.model_validate_json(resp)

    def update(self, account_id: str, page_id: str, params: dict) -> StatusPage:
        resp = self._client.request("PUT", _page_path(account_id, page_id), json=params)
        return StatusPage.model_validate_json(resp)

    def delete(self, account_id: str, page_id: str) -> None:
        self._client.request("DELETE", _page_path(account_id, page_id))

    # --- Component groups ---

    def create_component_group(self, account_id: str, page_id: str, params: dict) -> ComponentGroup:
        resp = self._client.request("POST", _page_path(account_id, page_id) + "/component-groups", json=params)
        return ComponentGroup.model_validate_json(resp)

    def list_component_groups(self, account_id: str, page_id: str) -> list[ComponentGroup]:
        resp = self._client.request("GET", _page_path(account_id, page_id) + "/component-groups")
        return [ComponentGroup.model_validate(g) for g in json.loads(resp)]

    def get_component_group(self, account_id: str, page_id: str, group_id: str) -> ComponentGroup:
        groups = self.list_component_groups(account_id, page_id)
        for g in groups:
            if g.id == group_id:
                return g
        from oack._exceptions import NotFoundError

        raise NotFoundError("component group not found")

    def update_component_group(self, account_id: str, page_id: str, group_id: str, params: dict) -> ComponentGroup:
        resp = self._client.request(
            "PUT",
            _page_path(account_id, page_id) + f"/component-groups/{group_id}",
            json=params,
        )
        return ComponentGroup.model_validate_json(resp)

    def delete_component_group(self, account_id: str, page_id: str, group_id: str) -> None:
        self._client.request("DELETE", _page_path(account_id, page_id) + f"/component-groups/{group_id}")

    # --- Components ---

    def create_component(self, account_id: str, page_id: str, params: dict) -> Component:
        resp = self._client.request("POST", _page_path(account_id, page_id) + "/components", json=params)
        return Component.model_validate_json(resp)

    def list_components(self, account_id: str, page_id: str) -> list[Component]:
        resp = self._client.request("GET", _page_path(account_id, page_id) + "/components")
        return [Component.model_validate(c) for c in json.loads(resp)]

    def get_component(self, account_id: str, page_id: str, comp_id: str) -> Component:
        components = self.list_components(account_id, page_id)
        for c in components:
            if c.id == comp_id:
                return c
        from oack._exceptions import NotFoundError

        raise NotFoundError("component not found")

    def update_component(self, account_id: str, page_id: str, comp_id: str, params: dict) -> Component:
        resp = self._client.request("PUT", _page_path(account_id, page_id) + f"/components/{comp_id}", json=params)
        return Component.model_validate_json(resp)

    def delete_component(self, account_id: str, page_id: str, comp_id: str) -> None:
        self._client.request("DELETE", _page_path(account_id, page_id) + f"/components/{comp_id}")

    # --- Incidents ---

    def create_incident(self, account_id: str, page_id: str, params: dict) -> Incident:
        resp = self._client.request("POST", _page_path(account_id, page_id) + "/incidents", json=params)
        return Incident.model_validate_json(resp)

    def list_incidents(self, account_id: str, page_id: str) -> list[Incident]:
        resp = self._client.request("GET", _page_path(account_id, page_id) + "/incidents")
        return [Incident.model_validate(i) for i in json.loads(resp)]

    def get_incident(self, account_id: str, page_id: str, incident_id: str) -> Incident:
        resp = self._client.request("GET", _page_path(account_id, page_id) + f"/incidents/{incident_id}")
        return Incident.model_validate_json(resp)

    def update_incident(self, account_id: str, page_id: str, incident_id: str, params: dict) -> Incident:
        resp = self._client.request("PUT", _page_path(account_id, page_id) + f"/incidents/{incident_id}", json=params)
        return Incident.model_validate_json(resp)

    def delete_incident(self, account_id: str, page_id: str, incident_id: str) -> None:
        self._client.request("DELETE", _page_path(account_id, page_id) + f"/incidents/{incident_id}")

    def post_incident_update(
        self, account_id: str, page_id: str, incident_id: str, message: str, status: str
    ) -> IncidentUpdate:
        resp = self._client.request(
            "POST",
            _page_path(account_id, page_id) + f"/incidents/{incident_id}/updates",
            json={"body": message, "status": status},
        )
        return IncidentUpdate.model_validate_json(resp)

    # --- Maintenances ---

    def create_maintenance(self, account_id: str, page_id: str, params: dict) -> Maintenance:
        resp = self._client.request("POST", _page_path(account_id, page_id) + "/maintenances", json=params)
        return Maintenance.model_validate_json(resp)

    def list_maintenances(self, account_id: str, page_id: str) -> list[Maintenance]:
        resp = self._client.request("GET", _page_path(account_id, page_id) + "/maintenances")
        return [Maintenance.model_validate(m) for m in json.loads(resp)]

    def get_maintenance(self, account_id: str, page_id: str, maint_id: str) -> Maintenance:
        resp = self._client.request("GET", _page_path(account_id, page_id) + f"/maintenances/{maint_id}")
        return Maintenance.model_validate_json(resp)

    def update_maintenance(self, account_id: str, page_id: str, maint_id: str, params: dict) -> Maintenance:
        resp = self._client.request("PUT", _page_path(account_id, page_id) + f"/maintenances/{maint_id}", json=params)
        return Maintenance.model_validate_json(resp)

    def delete_maintenance(self, account_id: str, page_id: str, maint_id: str) -> None:
        self._client.request("DELETE", _page_path(account_id, page_id) + f"/maintenances/{maint_id}")

    def post_maintenance_update(
        self, account_id: str, page_id: str, maint_id: str, message: str, status: str
    ) -> MaintenanceUpdate:
        resp = self._client.request(
            "POST",
            _page_path(account_id, page_id) + f"/maintenances/{maint_id}/updates",
            json={"body": message, "status": status},
        )
        return MaintenanceUpdate.model_validate_json(resp)

    # --- Subscribers ---

    def list_subscribers(self, account_id: str, page_id: str) -> list[Subscriber]:
        resp = self._client.request("GET", _page_path(account_id, page_id) + "/subscribers")
        return [Subscriber.model_validate(s) for s in json.loads(resp)]

    def remove_subscriber(self, account_id: str, page_id: str, subscriber_id: str) -> None:
        self._client.request("DELETE", _page_path(account_id, page_id) + f"/subscribers/{subscriber_id}")

    # --- Incident templates ---

    def create_incident_template(self, account_id: str, page_id: str, params: dict) -> IncidentTemplate:
        resp = self._client.request("POST", _page_path(account_id, page_id) + "/incident-templates", json=params)
        return IncidentTemplate.model_validate_json(resp)

    def list_incident_templates(self, account_id: str, page_id: str) -> list[IncidentTemplate]:
        resp = self._client.request("GET", _page_path(account_id, page_id) + "/incident-templates")
        return [IncidentTemplate.model_validate(t) for t in json.loads(resp)]

    def update_incident_template(
        self, account_id: str, page_id: str, template_id: str, params: dict
    ) -> IncidentTemplate:
        resp = self._client.request(
            "PUT",
            _page_path(account_id, page_id) + f"/incident-templates/{template_id}",
            json=params,
        )
        return IncidentTemplate.model_validate_json(resp)

    def delete_incident_template(self, account_id: str, page_id: str, template_id: str) -> None:
        self._client.request("DELETE", _page_path(account_id, page_id) + f"/incident-templates/{template_id}")

    # --- Watchdogs ---

    def create_watchdog(self, account_id: str, page_id: str, comp_id: str, params: dict) -> Watchdog:
        resp = self._client.request(
            "POST", _page_path(account_id, page_id) + f"/components/{comp_id}/watchdogs", json=params
        )
        return Watchdog.model_validate_json(resp)

    def list_watchdogs(self, account_id: str, page_id: str, comp_id: str) -> list[Watchdog]:
        resp = self._client.request("GET", _page_path(account_id, page_id) + f"/components/{comp_id}/watchdogs")
        return [Watchdog.model_validate(w) for w in json.loads(resp)]

    def delete_watchdog(self, account_id: str, page_id: str, comp_id: str, watchdog_id: str) -> None:
        self._client.request(
            "DELETE", _page_path(account_id, page_id) + f"/components/{comp_id}/watchdogs/{watchdog_id}"
        )
