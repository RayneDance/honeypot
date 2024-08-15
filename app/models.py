from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, BigInteger, Boolean


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    guild_id = Column(BigInteger, unique=True, index=True)
    prefix = Column(String, default="!")
    welcome_channel = Column(BigInteger, nullable=True)
    welcome_message = Column(String, nullable=True)
    honeypot_channel = Column(BigInteger, nullable=True)
    global_bans_enabled = Column(Boolean, default=True)
    leave_channel = Column(BigInteger, nullable=True)
    leave_message = Column(String, nullable=True)
    mod_log_channel = Column(BigInteger, nullable=True)
    mute_role = Column(BigInteger, nullable=True)
    autorole = Column(BigInteger, nullable=True)
    autorole_remove = Column(Boolean, default=False)
    autorole_remove_delay = Column(Integer, default=0)
    mod_role = Column(BigInteger, nullable=True)
    admin_role = Column(BigInteger, nullable=True)
    log_channel = Column(BigInteger, nullable=True)
    log_message_delete = Column(Boolean, default=False)
    log_message_edit = Column(Boolean, default=False)
    log_member_join = Column(Boolean, default=False)
    log_member_remove = Column(Boolean, default=False)
    log_member_ban = Column(Boolean, default=False)
    log_member_unban = Column(Boolean, default=False)


class HoneyPotChannels(Base):
    __tablename__ = "honeypot_channels"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    guild_id = Column(BigInteger, ForeignKey("servers.guild_id"))
    channel_id = Column(BigInteger, unique=True, index=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))

class GuildBotAdmin(Base):
    __tablename__ = "guild_bot_admins"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    guild_id = Column(BigInteger, ForeignKey("servers.guild_id"))
    user_id = Column(String, ForeignKey("users.user_id"))
    bot_admin = Column(Boolean, default=False)


class ProtectedUsers(Base):
    __tablename__ = "protected_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    guild_id = Column(BigInteger, ForeignKey("servers.guild_id"))
    user_id = Column(String, ForeignKey("users.user_id"))


class GlobalBans(Base):
    __tablename__ = "global_bans"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True, unique=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    reason = Column(String, nullable=True)
    guild_id = Column(BigInteger, nullable=True)
    banned_at = Column(DateTime, nullable=True)
    unbanned_at = Column(DateTime, nullable=True)
    unbanned_by = Column(String, ForeignKey("users.user_id"), nullable=True)
    active = Column(Boolean, default=True)
