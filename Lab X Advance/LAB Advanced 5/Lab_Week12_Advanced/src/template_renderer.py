import os
import re
from string import Formatter

class TemplateRenderer:
    """Render {context_key} and ${ENVIRONMENT_VARIABLE} placeholders."""
    _env_pattern = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

    def render(self, template_string, context):
        if not isinstance(template_string, str):
            return template_string
        def replace_env(match):
            return os.getenv(match.group(1), match.group(0))
        rendered = self._env_pattern.sub(replace_env, template_string)
        try:
            return Formatter().vformat(rendered, (), _SafeContext(context))
        except (ValueError, IndexError) as exc:
            raise ValueError(f"Cannot render template {template_string!r}: {exc}") from exc

# ค้นหาคลาสนี้ในไฟล์แล้วแก้ให้เป็นรูปแบบนี้ครับ
class _SafeContext(dict):
    def __missing__(self, key):
        # หากระบุคีย์ย่อยแบบมีจุดทศนิยม เช่น config.email
        if '.' in key:
            parts = key.split('.')
            current = self.get(parts[0])
            for part in parts[1:]:
                if isinstance(current, dict) and part in current:
                    current = current[part]
                elif isinstance(current, (list, tuple)) and part.isdigit():
                    current = current[int(part)]
                else:
                    return f"{{{key}}}"  # คืนค่ากลับไปตรงๆ เมื่อหาไม่เจอ เพื่อหยุดลูปการค้นหาซ้ำ
            return current
        
        # กรณีคีย์ธรรมดาแล้วหาไม่เจอใน Environment/Context ให้ดึงจาก os.environ หรือคืนค่าเดิม
        import os
        if key in os.environ:
            return os.environ[key]
            
        return f"{{{key}}}"