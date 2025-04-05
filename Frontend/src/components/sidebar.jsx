import { Link } from "react-router-dom";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <Link to="/">داشبورد</Link>
      <Link to="/finance">مالی</Link>
      <Link to="/reports">گزارش‌ها</Link>
    </div>
  );
};

export default Sidebar;
