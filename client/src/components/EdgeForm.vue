<template>
    <el-dialog v-model="dialogVisible" title="Create an edge" width="40%" :before-close="cancelHandle">
        <el-form :model="form" label-width="120px">
            <el-form-item label="Input">
                <el-input v-model="form.input" />
            </el-form-item>
            <el-form-item label="Output">
                <el-input v-model="form.output" />
            </el-form-item>
            <div v-for="(item,index) in form.bracket_list" :key="index">
                <el-form-item label="Bracket type">
                    <el-radio-group v-model="item.bracket_type">
                        <el-radio label="Open" />
                        <el-radio label="Close" />
                    </el-radio-group>
                </el-form-item>
                <el-form-item label="Bracket number">
                    <el-input v-model="item.bracket_number" />
                </el-form-item>
                <el-form-item label="Bracket label">
                    <el-input v-model="item.bracket_label" />
                </el-form-item>
            </div>
            <div>
                <el-button style="margin-left:25%" type="primary" @click="addList">Add a bracket</el-button>
                <el-button type="primary" @click="deleteList">Delete a bracket</el-button>
            </div>
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
    name: 'EdgeForm',
    props: {
        dialogVisible: {
            type: Boolean,
            default: false,
        }
    },
    emits: ['update:dialogVisible','cancel','confirm'],
    setup(props,ctx) {
        const form = reactive({
            input: '',
            output: '',
            bracket_list: [],
        })

        const addList = () => {
            form.bracket_list.push({
                bracket_type: 'Open',
                bracket_number: '',
                bracket_label: '',
            });
        }

        const deleteList = () => {
            if (form.bracket_list.length > 0) {
                form.bracket_list.pop();
            }
        }

        const reset = () => {
            form.input = "";
            form.output = "";
            form.bracket_list = [];
        }

        const cancelHandle = () => {
            ctx.emit('update:dialogVisible',false);
            ctx.emit('cancel');
            reset();
        }

        const confirmHandle = () => {
            for (let i in form.bracket_list) {
                if (form.bracket_list[i].bracket_number == '') {
                    alert('You must fill in the "bracket_number" field, which is a positive integer that determines the type of the bracket.');
                    return;
                }
            }
            ctx.emit('update:dialogVisible',false);
            ctx.emit('confirm',form);
            reset();
        }

        return { form, addList, deleteList, cancelHandle, confirmHandle }
    },
}
</script>
<style scoped>
.dialog-footer button:first-child {
    margin-right: 10px;
}
</style>
