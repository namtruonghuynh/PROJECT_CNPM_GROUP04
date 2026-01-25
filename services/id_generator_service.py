"""Service để sinh ID cho các loại user với prefix"""
from data.users import load_users


class IDGeneratorService:
    """Service để sinh ID tự động cho user mới"""
    
    PREFIX_STUDENT = "sv"
    PREFIX_LECTURER = "gv"
    PREFIX_ADMIN = "admin"
    
    @staticmethod
    def get_next_id(role: str) -> str:
        """
        Sinh ID tiếp theo cho user dựa trên role.
        
        Args:
            role: Role của user ('student', 'lecturer', 'admin')
            
        Returns:
            ID mới có định dạng: sv001, gv001, admin001, ...
        """
        prefix = IDGeneratorService._get_prefix(role)
        next_number = IDGeneratorService._get_next_number(prefix)
        return f"{prefix}{next_number:03d}"
    
    @staticmethod
    def _get_prefix(role: str) -> str:
        """Lấy prefix dựa trên role"""
        role_lower = role.lower()
        if role_lower == "student":
            return IDGeneratorService.PREFIX_STUDENT
        elif role_lower == "lecturer":
            return IDGeneratorService.PREFIX_LECTURER
        elif role_lower == "admin":
            return IDGeneratorService.PREFIX_ADMIN
        else:
            raise ValueError(f"Invalid role: {role}")
    
    @staticmethod
    def _get_next_number(prefix: str) -> int:
        """Lấy số tiếp theo cho prefix"""
        max_number = 0
        # Load users từ file mỗi lần để đảm bảo dữ liệu mới nhất
        users_data = load_users()
        
        for user in users_data:
            user_id = user.get("id", "")
            if isinstance(user_id, str) and user_id.startswith(prefix):
                try:
                    # Lấy phần số từ ID (ví dụ: sv001 -> 1)
                    number = int(user_id[len(prefix):])
                    if number > max_number:
                        max_number = number
                except (ValueError, IndexError):
                    continue
        
        return max_number + 1
