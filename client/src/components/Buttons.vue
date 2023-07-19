<template>
    <ul>
        <li v-for="(title,index) in titles" :key="index"><button @click="clickHandle(index+1)" :class="(status == index+1)?'selected':''">{{ title }}</button></li>
    </ul>
</template>

<script>
export default {
    name: 'Buttons',
    data() {
        return {
            status: 0,
            titles: ["Add vertex", "Add edge", "Edit object", "Remove object", "Move", "Clear", "Save as JSON", "Upload JSON", "Download code"],
        }
    },
    methods: {
        clickHandle(id) {
            // testing
            if (this.status != id) {
                this.status = id;
            }
            // else if (this.status != id && id == 6) {
            //     this.status = 6;
            // }
            // else if (this.status != id && id == 7) {
            //     this.status = 7;
            // }
            // else if (this.status != id && id == 9) {
            //     this.status = 9;
            // }
            else {
                this.status = 0;
            }
            this.$emit("statusChanged", this.status);
            if (this.status == 6 || this.status == 8) {
                this.status = 0;
            }
        }
    },
}
</script>

<style scoped>
button {
    width: 100%;
    border: 1px solid;
    text-transform: uppercase;
    font-size: 95%;
    padding: 6% 12%;
    font-weight: 300;
    display: flex;
    align-items: center;
    justify-content: space-around;
    background: #031628;
    color: #4cc9f0;
    cursor: pointer;
    margin: 3%;
    border-radius: 3px;
}
button:hover, .selected {
    color: white;
    border: 0;
    background-color: #4cc9f0;
    -webkit-box-shadow: 10px 10px 99px 6px rgba(76,201,240,1);
    -moz-box-shadow: 10px 10px 99px 6px rgba(76,201,240,1);
    box-shadow: 10px 10px 99px 6px rgba(76,201,240,1);
}
button:active {
    background-color: #4ccaf089;
}
ul {
    list-style: none;
    margin-left: 1%;
    padding: 0px;
    width: 15%;
    height: 80%;
    float: left;
}
</style>