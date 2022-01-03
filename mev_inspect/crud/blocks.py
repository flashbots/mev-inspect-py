import io
from datetime import datetime
from typing import Any, List, Optional

from mev_inspect.schemas.blocks import Block


def delete_blocks(
    db_session,
    after_block_number: int,
    before_block_number: int,
) -> None:
    db_session.execute(
        """
        DELETE FROM blocks
        WHERE
            block_number >= :after_block_number AND
            block_number < :before_block_number
        """,
        params={
            "after_block_number": after_block_number,
            "before_block_number": before_block_number,
        },
    )
    db_session.commit()


def clean_csv_value(value: Optional[Any]) -> str:
    if value is None:
        return r"\N"
    return str(value).replace("\n", "\\n")


def write_blocks(
    db_session,
    blocks: List[Block],
) -> None:
    csv_file_like_object = io.StringIO()
    for block in blocks:
        csv_file_like_object.write(
            "|".join(
                map(
                    clean_csv_value,
                    (
                        block.block_number,
                        datetime.fromtimestamp(block.block_timestamp),
                    ),
                )
            )
            + "\n"
        )

    csv_file_like_object.seek(0)

    with db_session.connection().connection.cursor() as cursor:
        cursor.copy_from(csv_file_like_object, "blocks", sep="|")
