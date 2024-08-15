from app.database import SessionLocal
from app import models


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def read_prefix(message):
    if message.guild:
        with get_db() as db:
            server = db.query(models.Server).filter(models.Server.guild_id == message.guild.id).first()
            if server:
                return server.prefix
    return "!"

def set_honeypot_channel(ctx, channel_id):
    with get_db() as db:
        honeypot_channel = db.query(models.HoneyPotChannels).filter(models.HoneyPotChannels.guild_id == ctx.guild.id).first()
        if honeypot_channel:
            honeypot_channel.channel_id = channel_id
        else:
            honeypot_channel = models.HoneyPotChannels(guild_id=ctx.guild.id, channel_id=channel_id)
            db.add(honeypot_channel)
        db.commit()
    return f"Honeypot channel set to {channel_id}"


def get_honeypot_channel(ctx):
    with get_db() as db:
        honeypot_channel = db.query(models.HoneyPotChannels).filter(models.HoneyPotChannels.guild_id == ctx.guild.id).first()
        if honeypot_channel:
            return honeypot_channel.channel_id
    return None


def set_prefix(ctx, prefix):
    with get_db() as db:
        server = db.query(models.Server).filter(models.Server.guild_id == ctx.guild.id).first()
        if server:
            server.prefix = prefix
        else:
            server = models.Server(guild_id=ctx.guild.id, prefix=prefix)
            db.add(server)
        db.commit()
    return f"Prefix set to {prefix}"


def set_protected(ctx):
    with get_db() as db:
        user = db.query(models.User).filter(models.User.user_id == ctx.author.id).first()
        if not user:
            # Write user to database
            user = models.User(user_id=ctx.author.id)
            db.add(user)
            db.commit()
        protected = db.query(models.ProtectedUsers).filter(models.ProtectedUsers.user_id == ctx.author.id).first()
        if protected:
            return True
        else:
            protected = models.ProtectedUsers(guild_id=ctx.guild.id, user_id=ctx.author.id)
            db.add(protected)
            db.commit()
    return True


def check_protected(ctx):
    if ctx.author.guild_permissions.administrator:
        return True
    with get_db() as db:
        protected = db.query(models.ProtectedUsers).filter(models.ProtectedUsers.user_id == ctx.author.id).first()
        if protected:
            return True
    return False


def check_global_bans(ctx):
    with get_db() as db:
        # Check if global bans are enabled
        server = db.query(models.Server).filter(models.Server.guild_id == ctx.guild.id).first()
        if server and server.global_bans_enabled:
            global_ban = db.query(models.GlobalBans).filter(models.GlobalBans.user_id == ctx.id).first()
            if global_ban:
                return True
    return False


def global_bans_enabled(ctx):
    with get_db() as db:
        server = db.query(models.Server).filter(models.Server.guild_id == ctx.guild.id).first()
        if server:
            return server.global_bans_enabled
    return False


def add_global_ban(ctx):
    with get_db() as db:
        global_ban = db.query(models.GlobalBans).filter(models.GlobalBans.user_id == ctx.id).first()
        if not global_ban:
            global_ban = models.GlobalBans(user_id=ctx.id)
            db.add(global_ban)
            db.commit()
    return True


