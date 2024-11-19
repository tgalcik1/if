<template>
    <div class="map">
        <p>Map</p>
        <div class="window">

        </div>

    </div>
</template>

<style scoped>
.map{
    margin: 16px;
}

.window{
    width: 100%;
    height: 200px;
    border: 2px solid black;
    
    /* via https://gist.github.com/dfrankland/f6fed3e3ccc42e3de482b324126f9542 */
    background-image:
      linear-gradient(45deg, #bbb 25%, transparent 25%), 
      linear-gradient(135deg, #bbb 25%, transparent 25%),
      linear-gradient(45deg, transparent 75%, #bbb 75%),
      linear-gradient(135deg, transparent 75%, #bbb 75%);
    background-size:25px 25px;
    background-position:0 0, 12.5px 0, 12.5px -12.5px, 0px 12.5px;
    animation: scroll-checkerboard 2s linear infinite;
}

@keyframes scroll-checkerboard {
    0% {
        background-position: 0 0, 12.5px 0, 12.5px -12.5px, 0px 12.5px;
    }
    100% {
        background-position: 25px 25px, 37.5px 25px, 37.5px 12.5px, 25px 37.5px;
    }
}
</style>