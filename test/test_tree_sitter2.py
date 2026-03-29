from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple

from tree_sitter_languages import get_parser


@dataclass
class LuaEdit:
    start_byte: int
    end_byte: int
    new_text: str


class LuaTableEditor:
    """使用 tree-sitter 解析 Lua 表，原地替换/新增字段."""

    def __init__(self) -> None:
        self._parser = get_parser("lua")

    def update_field_by_path(
        self,
        lua_text: str,
        key_path: List[str],
        new_value: str,
    ) -> str:
        """按路径更新字段；不存在则插入.

        Args:
            lua_text: 原始 lua 文件内容.
            key_path: 字段路径，如
                ["datas.info3dnpc.Shape3dNpcAnim", "attack"].
            new_value: 新值文本（例如 "9" 或 "{...}" 或 "true"）.

        Returns:
            更新后的 lua 文本.

        Raises:
            ValueError: 无法定位 return table.
        """
        tree = self._parser.parse(bytes(lua_text, "utf-8"))
        root = tree.root_node
        table_node = self._find_return_table(root)
        if table_node is None:
            raise ValueError("未找到 return { } 根表")

        edits = self._build_edits_for_path(
            lua_text=lua_text,
            table_node=table_node,
            key_path=key_path,
            new_value=new_value,
        )
        return self._apply_edits(lua_text, edits)

    def _find_return_table(self, root) -> Optional[object]:
        for node in root.children:
            if node.type == "return_statement":
                for child in node.children:
                    if child.type == "table_constructor":
                        return child
        return None

    def _build_edits_for_path(
        self,
        lua_text: str,
        table_node,
        key_path: List[str],
        new_value: str,
    ) -> List[LuaEdit]:
        if not key_path:
            return []

        current_table = table_node
        for depth, key in enumerate(key_path):
            field = self._find_field_in_table(
                lua_text=lua_text,
                table_node=current_table,
                key=key,
            )
            is_last = depth == len(key_path) - 1
            if field is None:
                if is_last:
                    return [self._insert_field(lua_text, current_table, key, new_value)]
                return [self._insert_field(lua_text, current_table, key, "{ }")]

            if is_last:
                return [self._replace_field_value(lua_text, field, new_value)]

            value_node = self._get_field_value_node(field)
            if value_node is None or value_node.type != "table_constructor":
                return [self._replace_field_value(lua_text, field, "{ }")]

            current_table = value_node

        return []

    def _find_field_in_table(self, lua_text: str, table_node, key: str) -> Optional[object]:
        for field in table_node.children:
            if field.type != "field":
                continue
            field_key = self._get_field_key(lua_text, field)
            if field_key == key:
                return field
        return None

    def _get_field_key(self, lua_text: str, field_node) -> Optional[str]:
        for child in field_node.children:
            if child.type == "identifier":
                return lua_text[child.start_byte:child.end_byte]
            if child.type == "string":
                text = lua_text[child.start_byte:child.end_byte]
                return text.strip("\"'")
            if child.type == "number":
                return lua_text[child.start_byte:child.end_byte]
            if child.type == "table_index":
                inner = lua_text[child.start_byte:child.end_byte]
                return inner.strip("[]").strip("\"'")
        return None

    def _get_field_value_node(self, field_node) -> Optional[object]:
        for child in field_node.children:
            if child.type in {"table_constructor", "string", "number", "true", "false"}:
                return child
        return None

    def _replace_field_value(self, lua_text: str, field_node, new_value: str) -> LuaEdit:
        value_node = self._get_field_value_node(field_node)
        if value_node is None:
            return LuaEdit(field_node.end_byte, field_node.end_byte, new_value)

        return LuaEdit(
            start_byte=value_node.start_byte,
            end_byte=value_node.end_byte,
            new_text=new_value,
        )

    def _insert_field(self, lua_text: str, table_node, key: str, value: str) -> LuaEdit:
        indent = self._infer_indent(lua_text, table_node)
        insert_text = f"{indent}[\"{key}\"] = {value},\n"
        return LuaEdit(
            start_byte=table_node.end_byte - 1,
            end_byte=table_node.end_byte - 1,
            new_text=insert_text,
        )

    def _infer_indent(self, lua_text: str, table_node) -> str:
        line_start = lua_text.rfind("\n", 0, table_node.start_byte) + 1
        line_prefix = lua_text[line_start:table_node.start_byte]
        return line_prefix + "\t"

    def _apply_edits(self, lua_text: str, edits: List[LuaEdit]) -> str:
        if not edits:
            return lua_text
        edits = sorted(edits, key=lambda e: e.start_byte, reverse=True)
        result = lua_text
        for edit in edits:
            result = result[:edit.start_byte] + edit.new_text + result[edit.end_byte:]
        return result
    


from pathlib import Path

editor = LuaTableEditor()
lua_path = Path(r"d:\param_2024.lua")
text = lua_path.read_text(encoding="utf-8")

# 替换字段
text = editor.update_field_by_path(
    lua_text=text,
    key_path=["datas.info3dnpc.Shape3dNpcAnim", "attack"],
    new_value="12",
)

# 插入字段（不存在则添加）
text = editor.update_field_by_path(
    lua_text=text,
    key_path=["datas.info3dnpc.Shape3dNpcAnim", "attack2"],
    new_value="7",
)

lua_path.write_text(text, encoding="utf-8")