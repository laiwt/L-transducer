<template>
    <div>
        <h2>{{ message }}</h2>
    </div>
</template>

<script>
export default {
    name: 'Tips',
    props: {
        status: {
            type: Number,
            default: 0,
        }
    },
    data() {
        return {
            index: 0,
            messages: [
                "Use \"ADD VERTEX\" to add a vertex.",
                "Welcome to the L-Graph generator!",
            ],
            message: "Welcome to the L-Graph generator!",
            timer: null,
        }
    },
    created() { },
    mounted() {
        this.initTimer();
    },
    destroyed() {
        this.destroyTimer();
    },
    watch: {
        status: function (newStatus) {
            switch (newStatus) {
                case 0:
                    this.messages = [
                        "Welcome to the L-Graph generator!",
                        "Use \"ADD VERTEX\" to add a vertex.",
                    ];
                    break;
                case 1:
                    this.messages = [
                        "Click to create a vertex.",
                        "After that you can use \"EDIT OBJECT\" to change the type of the vertex.",
                        "You can also use \"ADD EDGE\" to connect two vertices.",
                    ];
                    break;
                case 2:
                    this.messages = [
                        "Select two vertices to create an edge.",
                        "Select the start point first, and then the end point.",
                        "Bracket number: 1-'()', 2-'[]', 3-'{}', 4-'<>'.",
                        "You can use \"EDIT OBJECT\" to edit the created edges.",
                    ];
                    break;
                case 3:
                    this.messages = [
                        "Select a vertex or an edge to edit.",
                    ];
                    break;
                case 4:
                    this.messages = [
                        "Select a vertex or an edge to remove.",
                    ];
                    break;
                case 5:
                    this.messages = [
                        "Drag a vertex to move it.",
                    ];
                    break;
                case 9:
                this.messages = [
                        "The code is being generated, please wait...",
                        "The code is being generated, please wait",
                        "The code is being generated, please wait.",
                        "The code is being generated, please wait..",
                    ];
                    break;
                case 10:
                this.messages = [
                        "The code has been successfully downloaded!",
                    ];
                    break;
                case 11:
                this.messages = [
                        "The file has been successfully downloaded!",
                    ];
                    break;
                default:
                    break;
            }
            this.index = 0;
            this.message = this.messages[0];
        }
    },
    methods: {
        initTimer() {
            this.timer = setInterval(() => {
                this.message = this.messages[this.index];
                this.index += 1;
                if (this.index >= this.messages.length) {
                    this.index = 0;
                }
            }, 3000);
        },
        destroyTimer() {
            clearInterval(this.timer);
            this.timer = null;
        },
    }
}
</script>

<style scoped>
div {
    width: 80%;
    height: 5%;
    margin-left: 20%;
    margin-top: 1%;
}
h2 {
    color: white;
    margin-top: 0px;
    margin-left: 1%;
}
</style>