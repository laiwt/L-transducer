<template>
    <el-dialog
        :modal="true"
        :modal-append-to-body="false"
        title="Uploading"
        width="50%"
        v-model="dialogVisible"
        :before-close="handleClose">
        <div>
            <div class="file-box"
                :class="dropType ? 'dropbox-shadow' : ''"
                type="file"
                @dragenter.stop.prevent="fileBoxDragenter(true)"
                @dragleave.stop.prevent="fileBoxDragleave"
                @drop.stop.prevent="fileBoxDrop($event, true)"
                @dragover.stop.prevent=""
                @click="openFile">
                <div><i class="el-icon-upload upload-icon"></i></div>
                <div class="upload-text">
                    <span>Drag the file here, or</span>
                    <span>click to upload</span>
                </div>
            </div>
                <input ref="inputfile" class="file-content" type="file" :multiple="multiple" @change="inputFile">
        </div>
    </el-dialog>
</template>

<script>
export default {
    props: {
        dialogVisible: {
            type: Boolean,
            default: false
        },
        fileType: {
            type: String,
            default: 'json'
        },
        multiple: {
            type: Boolean,
            default: false
        }
    },
    data() {
        return {
            dropType: false,
            boxLock: false,
            innerHTMLList: [],
        }
    },
    mounted() {
    },
    methods: {
        handleClose() {
            this.$emit('update:dialogVisible', false)
            this.dropType = false
            this.boxLock = false
            this.innerHTMLList = []
        },
        inputFile(e) {
            this.readFile(e.target.files)
        },
        openFile() {
            this.$refs.inputfile.click()
        },
        fileBoxDragenter(flag) {
            this.boxLock = true
            setTimeout(() => {
                this.boxLock = false
            }, 10)
            this.dropType = flag
        },
        fileBoxDragleave() {
            if (this.boxLock) return
            this.dropType = false
        },
        fileBoxDrop(e) {
            this.dropType = false
            const isDirectory = e.dataTransfer.items[0].webkitGetAsEntry().isDirectory
            let fileList = e.dataTransfer.files
            if (isDirectory) {
                alert('Upload folders are not supported!')
                return
            }
            this.readFile(fileList)
        },
        readFile(fileList) {
            if(!this.multiple && fileList.length !== 1) {
                alert('Multiple file uploads are not supported!')
                return
            }
            let filterFileType = Object.keys(fileList).filter(item => {
                if (fileList[item].name.split('.')[1] !== this.fileType) {
                    return true
                }
                return false
            })
            if(filterFileType.length !== 0) {
                alert('Only supports uploading files in ' + this.fileType + ' format.')
                return
            }
            Object.keys(fileList).forEach(item => {
                const reader = new FileReader()
                reader.readAsText(fileList[item], 'utf8')
                reader.onload = () => {
                    this.innerHTMLList.push(reader.result)
                    this.$emit('submit', this.innerHTMLList)
                }
                reader.onerror = () => {
                    console.log('onError')
                }
            })
            this.handleClose()
        }
    }
}
</script>

<style lang="less" scoped>
/deep/ .el-upload {
    width: 100%;
}
/deep/ .el-upload-dragger {
    width: 100%;
}
.file-box {
    width: 100%;
    height: 180px;
    border: 1px dashed #d9d9d9;
    border-radius: 6px;
    cursor: pointer;
    background-color: #fff;
    text-align: center;
    box-sizing: border-box;
    padding-top: 50px;
}
.file-box:hover {
    border-color: #409eff;
}
.file-content {
    display: none;
}
.upload-icon {
    color: #c0c4cc;
    font-size: 67px;
}
.upload-text {
    color: #606266;
    font-size: 16px;
    & > span:nth-child(2) {
        margin-left: 4px;
        color: #409eff;
    }
}
.dropbox-shadow {
    box-shadow: 0px 0px 12px #409eff;
}
</style>
