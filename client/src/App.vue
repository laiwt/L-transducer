<template>
  <div id="header">
    <h1>L-Graph Generator</h1>
    <h3>Create your own L-Graph here!</h3>
  </div>
  <hr color="aqua"/>
  <Buttons @statusChanged="setStatus"/>
  <Tips :status="status"/>
  <Screen :status="status" @statusChanged="setStatus"/>
</template>

<script>
import Buttons from "./components/Buttons.vue"
import Tips from "./components/Tips.vue"
import Screen from "./components/Screen.vue"

export default {
  name: 'App',
  components: {
    Buttons,
    Tips,
    Screen,
  },
  data() {
    return {
      status: 0,
    }
  },
  methods: {
    setStatus(newStatus) {
      this.status = newStatus;
    },
  },
}
</script>

<style scoped>
#header {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #4cc9f0;
  height: 10%;
}
h1 {
  font-family: "Times New Roman", serif, sans-serif;
  margin-top: 1%;
  margin-bottom: 0px;
}
h3 {
  margin-top: 0.5%;
}
</style>