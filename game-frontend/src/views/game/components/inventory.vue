<template>
    <div class="inventory">
        <p>Inventory</p>

        <div class="grid">
            <div class="item-slot" v-for="(item, index) in inventory" :key="index">
                <img
                    :src="item ? `/items/${item}` : 'https://placehold.co/32x32'"
                    alt="."
                    style="width: 100%"
                />
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'Inventory',
    data() {
        return {
            maxItems: 64,
            inventory: Array(64).fill(null),
        };
    },
    methods: {
        updateInventory(newInventory) {
            this.inventory = Array.from({ length: this.maxItems }, (_, i) => newInventory[i] || null);
        }
    },
    mounted() {
        if (window.api && window.api.receive) {
            window.api.receive('fromMain', (data) => {
                if (data.type === 'inventory-update') {
                    this.updateInventory(data.inventory);
                }
            });
        }
    },
};
</script>

<style scoped>
.inventory {
    margin: 16px;
}

.grid {
    box-sizing: border-box;
    width: 100%;
    background: white;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(32px, 1fr));
    border: 2px solid black;
}

.item-slot img {
    width: 100%;
    image-rendering: pixelated;
    image-rendering: crisp-edges;
}
</style>
