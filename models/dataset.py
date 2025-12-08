class Dataset:
    """Represents a data science dataset in the platform."""

    def __init__(
        self,
        dataset_id: int,
        name: str,
        rows: int,
        columns: int,
        uploaded_by: str,
        upload_date: str,
    ):
        self.__id = dataset_id
        self.__name = name
        self.__rows = rows
        self.__columns = columns
        self.__uploaded_by = uploaded_by
        self.__upload_date = upload_date

    #Getters
    def get_id(self) -> int:
        return self.__id

    def get_name(self) -> str:
        return self.__name

    def get_rows(self) -> int:
        return self.__rows

    def get_columns(self) -> int:
        return self.__columns

    def get_uploaded_by(self) -> str:
        return self.__uploaded_by

    def get_upload_date(self) -> str:
        return self.__upload_date

    #Calculated value
    def get_size_estimate(self) -> int:
        """
        Estimate dataset size roughly based on rows * columns.
        (Simple logic required by the coursework)
        """
        return self.__rows * self.__columns

    def __str__(self) -> str:
        return (
            f"Dataset({self.__name}, rows={self.__rows}, "
            f"columns={self.__columns}, uploaded_by={self.__uploaded_by})"
        )

    #Convert to dict for dashboard
    def to_dict(self) -> dict:
        return {
            "ID": self.__id,
            "Name": self.__name,
            "Rows": self.__rows,
            "Columns": self.__columns,
            "Uploaded By": self.__uploaded_by,
            "Upload Date": self.__upload_date,
        }