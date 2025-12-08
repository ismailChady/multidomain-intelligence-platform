class SecurityIncident:
    """Represents a cybersecurity incident in the platform."""

    def __init__(
        self,
            incident_id: int,
            timestamp: str,
            severity: str,
            category: str,
            status: str,
            description: str,
    ):
        self.__id = incident_id
        self.__timestamp = timestamp
        self.__severity = severity
        self.__category = category
        self.__status = status
        self.__description = description

    #Getters

    def get_id(self) -> int:
        return self.__id

    def get_timestamp(self) -> str:
        return self.__timestamp

    def get_severity(self) -> str:
        return self.__severity

    def get_category(self) -> str:
        return self.__category

    def get_status(self) -> str:
        return self.__status

    def get_description(self) -> str:
        return self.__description

   

    def update_status(self, new_status: str) -> None:
        """Update the current status of the incident."""
        self.__status = new_status

    def get_severity_level(self) -> int:
        """
        Map severity to a numeric level.

        low -> 1, medium -> 2, high -> 3, critical -> 4, unknown -> 0
        """
        mapping = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4,
        }
        return mapping.get(self.__severity.lower(), 0)

    def is_high_risk(self) -> bool:
        """
        Return True if this incident is considered high risk.

        Here we treat 'High' and 'Critical' as high risk.
        """
        return self.__severity.lower() in ("high", "critical")

    #SERIALISATION FOR DATAFRAME / DISPLAY

    def to_dict(self) -> dict:
        """Return a dictionary representation, for DataFrame or JSON."""
        return {
            "incident_id": self.__id,
            "timestamp": self.__timestamp,
            "severity": self.__severity,
            "category": self.__category,
            "status": self.__status,
            "description": self.__description,
        }

    def __str__(self) -> str:
        return (
            f"Incident {self.__id} "
            f"[{self.__severity.upper()}] {self.__category} – {self.__status}"
        )