from sqlalchemy import MetaData, Integer, String, ForeignKey, Table, Column, JSON, ARRAY, DateTime, Boolean

metadata = MetaData()

Client = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True,),
    Column("lastName",  String, nullable=False),
    Column("firstName", String, nullable=False),
    Column("username", String, nullable=False),
    Column("hashed_password",  String, nullable=False),
    Column("role_id", Integer, ForeignKey("role.id"), nullable=False),
    Column("email", String(320), unique=True, index=True, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False)
)

Hospitals = Table(
    "hospital", 
    metadata, 
    Column("id", Integer, primary_key=True, nullable=False),
    Column("name", String, nullable=False),
    Column("address ", String, nullable=False),
    Column("contactPhone", String, nullable=False),
    Column("rooms", ARRAY(String), nullable=False),



)

Timetable = Table(
    "timetable", 
    metadata,
    Column("id", Integer, primary_key=True),
    Column("hospitalId", Integer, ForeignKey("hospital.id")),
    Column("doctorId", Integer, ForeignKey("user.id")),
    Column("from", DateTime, nullable=False),
    Column("to", DateTime, nullable=False),
    Column("room", String, nullable=False),

)

History = Table(
    "history", 
    metadata, 
    Column("id", Integer, primary_key=True),
    Column("date", DateTime, nullable=False),
    Column("pacientId", Integer, ForeignKey("user.id")),
    Column("hospitalId", Integer, ForeignKey("hospital.id")),
    Column("doctorId", Integer, ForeignKey("user.id")),
    Column("room", String, nullable=False),
    Column("data", String, nullable=False)
)


Role = Table(
    "role", 
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permission", JSON)
)