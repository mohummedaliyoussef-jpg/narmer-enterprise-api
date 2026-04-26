from logging.config import fileConfig
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import pool

from alembic import context

# تحميل متغيرات البيئة من ملف .env
load_dotenv()

# هذا كائن تهيئة Alembic
config = context.config

# إعداد تسجيل الأخطاء من الملف إن وُجد
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# ضع Metadata الخاصة بنماذجك هنا (اختياري حاليًا)
target_metadata = None

def run_migrations_offline() -> None:
    """تشغيل الترحيلات في وضع 'offline'."""
    url = os.getenv("DATABASE_URL")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """تشغيل الترحيلات في وضع 'online'."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise ValueError("DATABASE_URL غير موجود في متغيرات البيئة.")

    connectable = create_engine(url, poolclass=pool.NullPool)

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
