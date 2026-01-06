import React from 'react';

const Layout = ({ children }) => {
    return (
        <div className="app-container">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h2 className="sidebar-title">CloudSync</h2>
                </div>
                <nav>
                    <ul className="nav-links">
                        <li className="nav-item active">Dashboard</li>
                        <li className="nav-item">Files</li>
                        <li className="nav-item">Integrations</li>
                        <li className="nav-item">Settings</li>
                    </ul>
                </nav>
            </aside>

            <main className="main-content">
                <header className="top-bar">
                    <h1 className="page-title">Image Import</h1>
                    <div className="user-profile">
                        {/* Placeholder for user profile if needed later */}
                        <span style={{ fontWeight: 500 }}>Admin User</span>
                    </div>
                </header>

                <div className="content-wrapper">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default Layout;
