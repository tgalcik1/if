<template>
    <div class="navbar">
        <p style="margin-left: 16px">Heir of the Profane</p>
        <div>
            <button style="height: 40px" disabled>Settings</button>
            <button style="height: 40px" @click="this.$router.push('/')">Return to Title</button>
        </div>
    </div>
</template>

<style scoped>
.navbar {
    margin-top: -8px;
    margin-left: -8px;
    width: 100vw;
    display: flex;
    background: black;
    height: 40px;
    justify-content: space-between;
    align-items: center;
    color: white;
    align-items: center;
    position: relative;
    z-index: 10;
    box-shadow: -4px 0px 4px 5px rgba(0, 0, 0, 0.2);
}

</style>