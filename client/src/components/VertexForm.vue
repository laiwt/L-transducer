<template>
    <el-dialog v-model="dialogVisible" title="Set vertex type" width="30%" :before-close="cancelHandle">
        <el-form :model="form" label-width="120px">
            <el-form-item label="Vertex type">
                <el-radio-group v-model="form.type">
                    <el-radio label="Start" />
                    <el-radio label="Normal" />
                    <el-radio label="End" />
                </el-radio-group>
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="cancelHandle">Cancel</el-button>
                <el-button type="primary" @click="confirmHandle">Confirm</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script>
import { reactive } from 'vue'

export default {
    name: 'VertexForm',
    props: {
        dialogVisible: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['update:dialogVisible','cancel','confirm'],
    setup(props,ctx) {
        const form = reactive({
            type: "Normal",
        })

        const reset = () => {
            form.type = "Normal";
        }

        const cancelHandle = () => {
            ctx.emit('update:dialogVisible',false);
            ctx.emit('cancel');
            reset();
        }

        const confirmHandle = () => {
            ctx.emit('update:dialogVisible',false);
            ctx.emit('confirm',form.type);
            reset();
        }

        return { form, cancelHandle, confirmHandle }
    },
}
</script>
<style scoped>
.dialog-footer button:first-child {
    margin-right: 10px;
}
</style>
