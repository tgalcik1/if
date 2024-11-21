<template>
    <div class="quests">
        <p>Quests</p>

        <div class="quest-list">
            <div class="unlocked-quest" v-for="(quest, index) in unlockedQuests" :key="index">
                <p>{{ quest.name }}</p>
                <!-- <p>{{ quest.description }}</p> -->
            </div>

            <div class="completed-quest" v-for="(quest, index) in completedQuests" :key="index">
                <p>
                    <span style="text-decoration: line-through;">
                        {{ quest.name }}
                    </span>
                Completed</p>
                <!-- <p>{{ quest.description }}</p> -->
            </div>
        </div>
    </div>
</template>

<script>

export default{
    name: 'QuestLog',
    data(){
        return {
            unlockedQuests: [],
            completedQuests: []
        }
    },
    methods: {
        unlockQuest(name, description){
            this.unlockedQuests.push({name, description});
        },
        completeQuest(name, description){
            // find index of quest in unlockedQuests and remove
            let index = this.unlockedQuests.findIndex(quest => quest.name == name);
            if (index !== -1) {
                this.unlockedQuests.splice(index, 1);
            }

            this.completedQuests.push({name, description});
        },
    },
    mounted() {
        
        // get only quest output
        if (window.api && window.api.receive) {
            window.api.receive('fromMain', (data) => {
                if (['quest-unlock', 'quest-complete'].includes(data.type)){
                    if (data.type == 'quest-unlock'){
                        this.unlockQuest(data.name, data.description);
                    }
                    else if (data.type == 'quest-complete'){
                        this.completeQuest(data.name, data.description);
                    }
                }
            });
        }
    }
}
</script>

<style scoped>
.quests {
    display: flex;
    flex-direction: column;
    height: 100%;
    margin: 16px;
    overflow: hidden;
}

.quest-list {
    width: 100%;
    flex-grow: 1;
    overflow-y: auto;
    overflow-x: hidden;
    display: flex;
    flex-direction: column;
    border: 2px solid black;
    box-sizing: border-box;
    
    background-image:
      linear-gradient(45deg, #bbb 25%, transparent 25%), 
      linear-gradient(135deg, #bbb 25%, transparent 25%),
      linear-gradient(45deg, transparent 75%, #bbb 75%),
      linear-gradient(135deg, transparent 75%, #bbb 75%);
    background-size: 25px 25px;
    background-position: 0 0, 12.5px 0, 12.5px -12.5px, 0px 12.5px;
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


.unlocked-quest, .completed-quest{
    padding: 8px;
    border-bottom: 2px solid black;
}

.unlocked-quest{
    background-color: white;
}

.unlocked-quest:hover{
    cursor: pointer;
    background-color: rgb(200, 200, 200);
}

.completed-quest{
    background-color: rgba(0,0,0,0.6);
    color: rgb(220, 220, 220);
}

.quest-list::-webkit-scrollbar {
    width: 10px;
}

.quest-list::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0);
}

.quest-list::-webkit-scrollbar-thumb {
    background-color: rgba(0,0,0,0.25);
    border-radius: 5px;
    border: 2px solid #ccc;
}

.quest-list::-webkit-scrollbar-thumb:hover {
    background-color: rgba(0,0,0,0.5);
}

</style>