// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyDhRz_dOz2yzuKZTboTl_93v4vdn5gMdKE",
  authDomain: "vidyanxt-force.firebaseapp.com",
  projectId: "vidyanxt-force",
  storageBucket: "vidyanxt-force.firebasestorage.app",
  messagingSenderId: "943120617790",
  appId: "1:943120617790:web:4ea11b4bb61bf73ba41c6f",
  measurementId: "G-JSR40J7KM4"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);