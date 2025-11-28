const app = {
    state: {
        currentView: 'dashboard',
        isAuthenticated: false
    },

    init: function () {
        console.log("App Initialized");
        // Auth state is now handled by firebase.onAuthStateChanged in auth.js
    },

    // --- Auth Logic ---
    login: function (skipAnimation = false) {
        this.state.isAuthenticated = true;


        const authContainer = document.getElementById('auth-container');
        const appContainer = document.getElementById('app-container');

        if (skipAnimation) {
            authContainer.classList.add('hidden');
            appContainer.classList.remove('hidden');
        } else {
            // Fade out auth, fade in app
            authContainer.style.opacity = '0';
            setTimeout(() => {
                authContainer.classList.add('hidden');
                appContainer.classList.remove('hidden');
                // Reset opacity for next time
                authContainer.style.opacity = '1';
            }, 300);
        }
    },

    logout: function () {
        this.state.isAuthenticated = false;


        document.getElementById('app-container').classList.add('hidden');
        document.getElementById('auth-container').classList.remove('hidden');
        this.switchAuth('login');
    },

    showAuth: function () {
        document.getElementById('auth-container').classList.remove('hidden');
        document.getElementById('app-container').classList.add('hidden');
    },

    switchAuth: function (viewId) {
        document.querySelectorAll('.auth-view').forEach(el => el.classList.remove('active'));
        document.getElementById('view-' + viewId).classList.add('active');
    },

    // --- Navigation Logic ---
    navigate: function (viewId) {
        // Update Sidebar Active State
        document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));
        // Find the nav item that triggered this (or find by onclick attribute if called programmatically)
        const navItems = document.querySelectorAll('.nav-item');
        for (let item of navItems) {
            if (item.getAttribute('onclick').includes(viewId)) {
                item.classList.add('active');
                break;
            }
        }

        // Hide all views
        document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active'));

        // Show target view
        const targetView = document.getElementById('view-' + viewId);
        if (targetView) {
            targetView.classList.add('active');
            this.state.currentView = viewId;

            // Update Page Title
            const titles = {
                'dashboard': 'Overview',
                'groups': 'Manage Groups',
                'chats': 'Single Chats',
                'contacts': 'Contacts',
                'agents': 'AI Agents',
                'logs': 'System Logs',
                'settings': 'Settings'
            };
            document.getElementById('page-title').innerText = titles[viewId] || 'Dashboard';
        }
    },

    // --- Modal Logic ---
    openModal: function (modalId) {
        const overlay = document.getElementById('modal-overlay');
        const modal = document.getElementById('modal-' + modalId);

        // Hide any currently open modals
        document.querySelectorAll('.modal').forEach(el => el.classList.remove('active'));

        if (modal) {
            overlay.classList.remove('hidden');
            // Small delay to allow display:flex to apply before adding active class for opacity transition
            setTimeout(() => {
                overlay.classList.add('active');
                modal.classList.add('active');
            }, 10);
        }
    },

    closeModal: function (event, force = false) {
        // If triggered by overlay click, ensure we didn't click inside the modal
        if (!force && event && event.target !== event.currentTarget) return;

        const overlay = document.getElementById('modal-overlay');
        overlay.classList.remove('active');

        // Wait for transition to finish before hiding
        setTimeout(() => {
            overlay.classList.add('hidden');
            document.querySelectorAll('.modal').forEach(el => el.classList.remove('active'));
        }, 200);
    }
};

// Start the app
document.addEventListener('DOMContentLoaded', () => {
    app.init();
});
