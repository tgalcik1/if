<template>
    <div class="sidebar">
        <Map/>
        <Inventory/>
        <Quests/>
    </div>
</template>

<script>
import Map from './map.vue';
import Inventory from './inventory.vue';
import Quests from './quests.vue';

export default {
    name: 'Sidebar',
    components:
    {
        Map,
        Inventory,
        Quests
    }
};
</script>

<style scoped>
.sidebar{
    position: absolute;
    right: 0;
    background: lightgray;
    width: 300px;
    height: calc(100vh - 40px);
    box-shadow: -4px 0px 4px 1px rgba(0, 0, 0, 0.2);
    z-index: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border-left: 2px solid black;
}
</style>