<template>
    <div class="inventory">
        <p>Inventory</p>

        <div class="grid">
            <div class="item-slot" v-for="index in maxItems" :key="index">
                <img src="https://via.placeholder.com/50" alt="Item" style="width: 100%">
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Inventory',
    data() {
        return {
            maxItems: 56,
        };
    },
};
</script>

<style scoped>
.inventory {
    margin: 16px;
}

.grid {
    width: 100%;
    background: white;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(32px, 1fr));
    border: 2px solid black;
}
</style>
