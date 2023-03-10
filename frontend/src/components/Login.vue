<script setup>
    import { ref } from "vue";
    import { useAuth0 } from "@auth0/auth0-vue";
    import { ArrowLeftOnRectangleIcon, ArrowRightOnRectangleIcon } from "@heroicons/vue/20/solid";
    import AuthCard from "../Layouts/AuthCard.vue";

    // declarations & initializations
    const { loginWithRedirect, user, isAuthenticated } = useAuth0();
    const count = ref(0);

    // definitions
    defineProps({
        msg: String,
    });

    // functions
    const login = () => loginWithRedirect();
    const logout = () => {
        loginWithRedirect({
            returnTo: window.location.origin + '/logout',
        });
    };
</script>

<template>
    <AuthCard>
        <div class="flex justify-center flex-col align-middle p-5 min-h-60">
            <h1 class="text-2xl font-bold">Welcome Back!</h1>
            <p class="text-gray-400">{{ msg }}</p>
            <pre v-if="isAuthenticated" class="bg-gray-100 rounded-md p-2 text-xs font-mono text-left">
                <code>{{ user }}</code>
            </pre>
        </div>
        <template #footer>
            <div class="flex items-end justify-between w-full">
                <button v-if="!isAuthenticated"
                    type="button"
                    @click="login"
                    class="bg-gray-200 hover:bg-gray-100 dark:bg-gray-400 py-2 px-4 rounded flex align-middle gap-2"
                >
                    <ArrowRightOnRectangleIcon class="text-gray-800 h-5 w-5" />Sign In
                </button>
                <button v-if="isAuthenticated"
                    type="button"
                    @click="logout"
                    class="bg-gray-200 hover:bg-gray-100 dark:bg-gray-400 py-2 px-4 rounded flex align-middle gap-2"
                >
                    <ArrowLeftOnRectangleIcon class="text-gray-800 h-5 w-5" />Sign Out</button>
                <span class="text-xs">Powered by Auth0</span>
            </div>
        </template>
    </AuthCard>
</template>
