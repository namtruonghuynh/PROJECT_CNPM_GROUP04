import json
from datetime import datetime


class RegistrationPeriodService:

    @staticmethod
    def check_period():
        """Check if registration period is open"""
        try:
            with open("data/registration_periods.json", "r", encoding="utf-8") as f:
                periods = json.load(f)
            
            # Find active period
            for period in periods:
                start = datetime.fromisoformat(period["start_date"])
                end = datetime.fromisoformat(period["end_date"])
                
                if start <= datetime.now() <= end:
                    return True, "Registration period is open"
            
            return False, "Registration period is closed"
        except:
            return False, "No registration period configured"

    @staticmethod
    def get_active_period():
        """Get current active registration period"""
        try:
            with open("data/registration_periods.json", "r", encoding="utf-8") as f:
                periods = json.load(f)
            
            for period in periods:
                start = datetime.fromisoformat(period["start_date"])
                end = datetime.fromisoformat(period["end_date"])
                
                if start <= datetime.now() <= end:
                    return period
            
            return None
        except:
            return None

    @staticmethod
    def get_all_periods():
        """Get all registration periods"""
        try:
            with open("data/registration_periods.json", "r", encoding="utf-8") as f:
                periods = json.load(f)
            return periods
        except:
            return []

    @staticmethod
    def add_period(name, start_date, end_date):
        """Add new registration period"""
        try:
            with open("data/registration_periods.json", "r", encoding="utf-8") as f:
                periods = json.load(f)
        except:
            periods = []

        # Generate new ID
        new_id = max([p["period_id"] for p in periods], default=0) + 1

        new_period = {
            "period_id": new_id,
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "created_at": datetime.now().isoformat()
        }

        periods.append(new_period)

        with open("data/registration_periods.json", "w", encoding="utf-8") as f:
            json.dump(periods, f, indent=4)

        return True, "Period added successfully"

    @staticmethod
    def update_period(period_id, name, start_date, end_date):
        """Update registration period"""
        try:
            with open("data/registration_periods.json", "r", encoding="utf-8") as f:
                periods = json.load(f)

            for period in periods:
                if period["period_id"] == period_id:
                    period["name"] = name
                    period["start_date"] = start_date
                    period["end_date"] = end_date
                    break
            else:
                return False, "Period not found"

            with open("data/registration_periods.json", "w", encoding="utf-8") as f:
                json.dump(periods, f, indent=4)

            return True, "Period updated successfully"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def delete_period(period_id):
        """Delete registration period"""
        try:
            with open("data/registration_periods.json", "r", encoding="utf-8") as f:
                periods = json.load(f)

            periods = [p for p in periods if p["period_id"] != period_id]

            with open("data/registration_periods.json", "w", encoding="utf-8") as f:
                json.dump(periods, f, indent=4)

            return True, "Period deleted successfully"
        except Exception as e:
            return False, str(e)