// Firebase Configuration
// IMPORTANT: You must replace these values with your actual Firebase Client Config
// You can find this in your Firebase Console -> Project Settings -> General -> Your apps
const firebaseConfig = {
    apiKey: "AIzaSyCk8Gi4_YMLQ732N1oInxjIkOGah1FsBDg",
    authDomain: "telegram-kato.firebaseapp.com",
    projectId: "telegram-kato",
    storageBucket: "telegram-kato.firebasestorage.app",
    messagingSenderId: "451651510126",
    appId: "1:451651510126:web:434f4bb943e805016c6b7f"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();

const authManager = {
    // Helper to save user to Firestore
    saveUserToFirestore: async function (user) {
        try {
            const userRef = db.collection('users').doc(user.uid);
            const doc = await userRef.get();

            // Only create/update if it doesn't exist or we want to update fields
            // Using set with merge: true is safe and idempotent
            await userRef.set({
                uid: user.uid,
                email: user.email,
                display_name: user.displayName || '',
                photo_url: user.photoURL || '',
                phone_number: user.phoneNumber || '',
                created_time: firebase.firestore.FieldValue.serverTimestamp()
            }, { merge: true });

            console.log("User document saved to Firestore");
        } catch (error) {
            console.error("Error saving user to Firestore:", error);
        }
    },

    // Sign Up
    signup: async function () {
        const name = document.querySelector('#view-signup input[type="text"]').value;
        const email = document.querySelector('#view-signup input[type="email"]').value;
        const password = document.querySelector('#view-signup input[type="password"]').value;

        try {
            const userCredential = await auth.createUserWithEmailAndPassword(email, password);
            // Update profile name
            await userCredential.user.updateProfile({
                displayName: name
            });

            // Create user document in Firestore
            await this.saveUserToFirestore(userCredential.user);

            console.log("User created:", userCredential.user);
        } catch (error) {
            alert("Error signing up: " + error.message);
        }
    },

    // Login
    login: async function () {
        const email = document.querySelector('#view-login input[type="text"]').value;
        const password = document.querySelector('#view-login input[type="password"]').value;

        try {
            await auth.signInWithEmailAndPassword(email, password);
            console.log("User logged in");
        } catch (error) {
            alert("Error logging in: " + error.message);
        }
    },

    // Google Login
    loginWithGoogle: async function () {
        const provider = new firebase.auth.GoogleAuthProvider();
        try {
            const result = await auth.signInWithPopup(provider);
            const user = result.user;

            // Create or update user document in Firestore
            await this.saveUserToFirestore(user);

            console.log("User logged in with Google:", user);
        } catch (error) {
            console.error("Google Sign-In Error:", error);
            alert("Google Sign-In failed: " + error.message);
        }
    },

    // Logout
    logout: async function () {
        try {
            await auth.signOut();
            app.logout(); // Update UI
        } catch (error) {
            console.error("Logout error", error);
        }
    },

    // Reset Password
    resetPassword: async function () {
        const email = document.getElementById('reset-email').value;
        if (!email) {
            alert("Please enter your email address.");
            return;
        }
        try {
            await auth.sendPasswordResetEmail(email);
            alert("Password reset email sent! Check your inbox.");
            app.switchAuth('login');
        } catch (error) {
            alert("Error: " + error.message);
        }
    },

    // Delete Account
    deleteAccount: async function () {
        if (confirm("Are you sure you want to delete your account? This cannot be undone.")) {
            try {
                const user = auth.currentUser;
                await user.delete();
                alert("Account deleted.");
            } catch (error) {
                alert("Error deleting account: " + error.message);
            }
        }
    }
};

// Auth State Observer
auth.onAuthStateChanged(async (user) => {
    if (user) {
        // User is signed in
        console.log("Auth State: Signed In", user.email);
        localStorage.setItem('isLoggedIn', 'true');

        // Update UI with user info
        const nameDisplay = document.querySelector('.user-info .name');
        const avatarDisplay = document.querySelector('.user-profile .avatar');

        // Try to get display name from Firestore if not in Auth profile (e.g. sometimes happens with email signup before profile update)
        let displayName = user.displayName;
        if (!displayName) {
            try {
                const doc = await db.collection('users').doc(user.uid).get();
                if (doc.exists) {
                    displayName = doc.data().display_name;
                }
            } catch (e) { console.log("Could not fetch user doc", e); }
        }

        if (nameDisplay) nameDisplay.textContent = displayName || user.email.split('@')[0];
        if (avatarDisplay) {
            if (user.photoURL) {
                avatarDisplay.innerHTML = `<img src="${user.photoURL}" style="width:100%;height:100%;border-radius:50%;">`;
            } else {
                avatarDisplay.textContent = (displayName || user.email)[0].toUpperCase();
            }
        }

        // Get ID token if needed for backend calls
        user.getIdToken().then((token) => {
            localStorage.setItem('authToken', token);
        });

        app.login(true); // Transition to app
    } else {
        // User is signed out
        console.log("Auth State: Signed Out");
        localStorage.removeItem('isLoggedIn');
        localStorage.removeItem('authToken');
        app.showAuth();
    }
});
