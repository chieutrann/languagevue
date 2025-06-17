// Firebase Authentication Integration for Main App
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.0.2/firebase-app.js';
import {
    getAuth,
    signInWithPopup,
    signInWithRedirect,
    getRedirectResult,
    GoogleAuthProvider,
    signOut
} from 'https://www.gstatic.com/firebasejs/11.0.2/firebase-auth.js';

let app, auth, provider;

document.addEventListener('DOMContentLoaded', function() {
    if (window.firebaseConfig) {
        initializeFirebase();
        handleRedirectResult();
    }
});

function initializeFirebase() {
    try {
        app = initializeApp(window.firebaseConfig);
        auth = getAuth(app);
        provider = new GoogleAuthProvider();
        provider.addScope('email');
        provider.addScope('profile');
        console.log('Firebase initialized successfully');
    } catch (error) {
        console.error('Firebase initialization error:', error);
    }
}

async function handleRedirectResult() {
    if (!auth) return;
    try {
        const result = await getRedirectResult(auth);
        if (result) {
            const user = result.user;
            const idToken = await user.getIdToken();
            await sendTokenToBackend(idToken);
        }
    } catch (error) {
        console.error('Redirect result error:', error);
        showError('Authentication failed. Please try again.');
    }
}

async function sendTokenToBackend(idToken) {
    try {
        const response = await fetch('/firebase-auth', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idToken: idToken })
        });
        const data = await response.json();
        if (data.success) {
            window.location.href = data.redirect;
        } else {
            showError('Authentication failed: ' + data.error);
        }
    } catch (error) {
        console.error('Backend authentication error:', error);
        showError('Authentication failed. Please try again.');
    }
}

export async function signInWithGoogle() {
    if (!auth || !provider) {
        console.error('Firebase not initialized');
        return;
    }
    try {
        showLoading(true);
        const result = await signInWithPopup(auth, provider);
        const user = result.user;
        const idToken = await user.getIdToken();
        await sendTokenToBackend(idToken);
    } catch (error) {
        console.error('Google sign-in error:', error);
        showError('Google sign-in failed. Please try again.');
    } finally {
        showLoading(false);
    }
}

export function signInWithGoogleRedirect() {
    if (!auth || !provider) {
        console.error('Firebase not initialized');
        return;
    }
    try {
        signInWithRedirect(auth, provider);
    } catch (error) {
        console.error('Google sign-in redirect error:', error);
        showError('Google sign-in failed. Please try again.');
    }
}

export async function signOutUser() {
    if (!auth) return;
    try {
        await signOut(auth);
        window.location.href = '/logout';
    } catch (error) {
        console.error('Sign out error:', error);
    }
}

function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show mt-3';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    const mainContent = document.querySelector('.main-content') || document.body;
    mainContent.insertBefore(alertDiv, mainContent.firstChild);
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 10000);
}

function showLoading(show) {
    const buttons = document.querySelectorAll('[id*="google"], [id*="Google"]');
    buttons.forEach(button => {
        if (show) {
            button.disabled = true;
            const originalText = button.innerHTML;
            button.setAttribute('data-original-text', originalText);
            button.innerHTML = '<div class="spinner"></div> Signing in...';
        } else {
            button.disabled = false;
            const originalText = button.getAttribute('data-original-text');
            if (originalText) {
                button.innerHTML = originalText;
            }
        }
    });
}

window.firebaseAuth = {
    signInWithGoogle,
    signInWithGoogleRedirect,
    signOutUser
};
