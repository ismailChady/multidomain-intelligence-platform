class ITTicket:
    """Represents an IT support ticket."""

    def __init__(
        self,
        ticket_id: int,
        priority: str,
        description: str,
        status: str,
        assigned_to: str,
        created_at: str,
        resolution_time: float,
    ):
        self.__id = ticket_id
        self.__priority = priority
        self.__description = description
        self.__status = status
        self.__assigned_to = assigned_to
        self.__created_at = created_at
        self.__resolution_time = resolution_time

    #Methods
    def assign_to(self, staff: str) -> None:
        self.__assigned_to = staff

    def update_status(self, new_status: str) -> None:
        self.__status = new_status

    def close_ticket(self) -> None:
        self.__status = "Closed"

    #Getters
    def get_id(self) -> int:
        return self.__id

    def get_priority(self) -> str:
        return self.__priority

    def get_status(self) -> str:
        return self.__status

    def get_description(self) -> str:
        return self.__description

    def get_created_at(self) -> str:
        return self.__created_at

    def get_resolution_time(self) -> float:
        return self.__resolution_time

    #Convert to dict
    def to_dict(self) -> dict:
        return {
            "Ticket ID": self.__id,
            "Priority": self.__priority,
            "Description": self.__description,
            "Status": self.__status,
            "Assigned To": self.__assigned_to,
            "Created At": self.__created_at,
            "Resolution Time": self.__resolution_time,
        }

    #Stringify
    def __str__(self) -> str:
        return (
            f"Ticket {self.__id}: {self.__priority} – "
            f"{self.__status} (assigned to: {self.__assigned_to})"
        )