<template>
    <div class="border-1 border-gray-50 border rounded-sm shadow-xl w-full">
        <section>
            <slot />
        </section>
        <footer class="bg-gray-50 flex justify-end p-5">
            <slot name="footer" />
        </footer>
    </div>
</template>