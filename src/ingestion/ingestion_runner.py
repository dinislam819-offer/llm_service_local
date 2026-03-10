# """
# Ingestion pipeline: загружает CSV датасета Avito в БД с эмбеддингами.

# Запуск:
#     uv run python -m src.ingestion.ingestion_runner --file data/train.csv --limit 10000
# """
# import asyncio
# import argparse
# import pandas as pd

# from src.ingestion.embedding_pipeline import EmbeddingPipeline
# from src.infrastructure.db.session import async_session_factory, create_db_and_tables


# async def run(csv_path: str, limit: int, batch_size: int = 100, only_cars: bool = False):
#     print(f"Создание таблиц...")
#     await create_db_and_tables()

#     print(f"Загрузка данных из {csv_path}...")
#     df = pd.read_csv(csv_path, nrows=limit)

#     # Фильтруем только автомобили (если флаг включен)
#     if only_cars and "category_name" in df.columns:
#         df = df[df["category_name"].str.contains("Авто|авто|Auto", na=False)]
#         print(f"Найдено объявлений об авто: {len(df)}")

#     # Убираем строки без заголовка
#     df = df.dropna(subset=["title"])
#     df["description"] = df["description"].fillna("")

#     pipeline = EmbeddingPipeline()

#     async with async_session_factory() as session:
#         total = 0
#         for start in range(0, len(df), batch_size):
#             batch = df.iloc[start : start + batch_size]
#             await pipeline.process_batch(batch, session)
#             total += len(batch)
#             print(f"Обработано: {total}/{len(df)}")

#         await session.commit()

#     print(f"✅ Готово! Загружено {total} объявлений.")


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--file", required=True, help="Путь к CSV файлу")
#     parser.add_argument("--limit", type=int, default=10000, help="Максимум строк")
#     parser.add_argument("--batch", type=int, default=100, help="Размер батча")
#     parser.add_argument(
#         "--only-cars",
#         action="store_true",
#         help="Загружать только объявления об автомобилях",
#     )

#     args = parser.parse_args()

#     asyncio.run(
#         run(
#             csv_path=args.file,
#             limit=args.limit,
#             batch_size=args.batch,
#             only_cars=args.only_cars,
#         )
#     )

import asyncio
import argparse
import pandas as pd
import time

from src.ingestion.embedding_pipeline import EmbeddingPipeline
from src.infrastructure.db.session import async_session_factory, create_db_and_tables


async def run(csv_path: str, limit: int, batch_size: int = 100, only_cars: bool = False):
    print(f"Создание таблиц...")
    await create_db_and_tables()

    print(f"Загрузка данных из {csv_path}...")
    df = pd.read_csv(csv_path, nrows=limit)

    if only_cars and "category_name" in df.columns:
        df = df[df["category_name"].str.contains("Авто|авто|Auto", na=False)]
        print(f"Найдено объявлений об авто: {len(df)}")

    df = df.dropna(subset=["title"])
    df["description"] = df["description"].fillna("")

    pipeline = EmbeddingPipeline()

    async with async_session_factory() as session:
        total = 0
        for i, start in enumerate(range(0, len(df), batch_size)):
            batch = df.iloc[start : start + batch_size]
            await pipeline.process_batch(batch, session)
            total += len(batch)
            print(f"Обработано: {total}/{len(df)}")

            # Пауза каждые 90 запросов чтобы не превысить лимит 100/мин
            if total < len(df):
                print("Пауза 65 секунд (лимит Google API)...")
                await asyncio.sleep(65)

        await session.commit()

    print(f"✅ Готово! Загружено {total} объявлений.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Путь к CSV файлу")
    parser.add_argument("--limit", type=int, default=10000, help="Максимум строк")
    parser.add_argument("--batch", type=int, default=90, help="Размер батча")
    parser.add_argument(
        "--only-cars",
        action="store_true",
        help="Загружать только объявления об автомобилях",
    )

    args = parser.parse_args()

    asyncio.run(
        run(
            csv_path=args.file,
            limit=args.limit,
            batch_size=args.batch,
            only_cars=args.only_cars,
        )
    )