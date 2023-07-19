<template>
    <div>
        <svg ref="container" width="100%" height="100%" @click="createVertex">
        </svg>
    </div>
    <EdgeForm v-model:dialogVisible="edgeFormVisable" @cancel="cancelHandle" @confirm="confirmHandle"></EdgeForm>
    <VertexForm v-model:dialogVisible="vertexFormVisable" @cancel="cancelHandle_vertex" @confirm="confirmHandle_vertex"></VertexForm>
    <UploadFile v-model:dialogVisible="fileReadDialogVisable" fileType='json' :multiple="false" @submit="createFromJSON"></UploadFile>
</template>

<script>
import EdgeForm from './EdgeForm.vue'
import VertexForm from './VertexForm.vue'
import UploadFile from './UploadFile.vue'
import axios from 'axios'

export default {
    name: 'Screen',
    components: {
        EdgeForm,
        VertexForm,
        UploadFile,
    },
    props: {
        status: {
            type: Number,
            default: 0,
        }
    },
	data() {
		return {
			container: null,
            vertexId: 0,
            from: null,
            to: null,
            vertices: [],
            edges: [],
            edgeFormVisable: false,
            vertexFormVisable: false,
            fileReadDialogVisable: false,
            selectedVertex: null,
            vertices_upload: [],
            data_json: {vertices:[], edges:[]},
            path: "http://192.168.1.4:5000/download",
		};
	},
	methods: {
		initDom() {
			this.container = this.$refs.container;
		},
        createVertexWithCoordinate(offsetX, offsetY) {
            this.vertexId++;
            var oG = this.createTag("g",{"onclick":"clickHandle_window(this)"});
			var oC = this.createTag("circle",{"cx":offsetX,"cy":offsetY,"r":"30","fill":"aqua","stroke":"black","stroke-width":"1"});
            var oT = this.createTag("text",{"x":offsetX,"y":offsetY+8,"fill":"black","font-size":"20","text-anchor":"middle"});
            oT.innerHTML = this.vertexId;
            oG.appendChild(oC);
            oG.appendChild(oT);
			this.container.appendChild(oG);
            this.vertices.push({vertex:oG,type:"Normal"});
            this.vertices_upload.push({id:this.vertexId, type:"Normal", edges:[]});
            this.data_json.vertices.push({id:this.vertexId, x:offsetX, y:offsetY, type:"Normal"})
        },
		createVertex(e) {
            if (this.status != 1) {
                return;
            }
            this.createVertexWithCoordinate(e.offsetX, e.offsetY);
		},
		createTag(tag,objAttr) {
			var oTag = document.createElementNS("http://www.w3.org/2000/svg",tag);
			for (var attr in objAttr){
				oTag.setAttribute(attr, objAttr[attr]);
			}
			return oTag;
		},
        clickHandle(oG) {
            if (this.status == 2) {
                this.edgeFormVisable = false;
                if (this.from == null) {
                    this.from = oG;
                    return;
                }
                this.to = oG;
                this.edgeFormVisable = true;
            }
            else if (this.status == 3) {
                this.selectedVertex = oG;
                this.vertexFormVisable = true;
            }
            // else if (this.status == 4) {
            //     this.container.removeChild(oG);
            //     this.vertices = this.vertices.filter(item => item.vertex != oG);
            //     this.edges = this.edges.filter((item) => {
            //             if (item.from != oG && item.to != oG) {
            //                 return true;
            //             }
            //             else {
            //                 this.container.removeChild(item.edge);
            //                 // todo: delete
            //                 return false;
            //             }
            //         });
            //     this.edges = this.edges.filter((item) => {
            //             if (item.edge != oG) {
            //                 return true;
            //             }
            //             else {
            //                 let id_from = item.from.lastChild.innerHTML;
            //                 let id_to = item.to.lastChild.innerHTML;
            //                 for (let i in this.vertices_upload) {
            //                     if (this.vertices_upload[i].id == id_from) {
            //                         // this.vertices_upload[i].edges = this.vertices_upload[i].edges.filter(item => item.to != id_to);
            //                     }
            //                 }
            //                 return false;
            //             }
            //         });
            //     // var id = oG.lastChild.innerHTML
            //     // this.vertices_upload = this.vertices_upload.filter(item => item.id != id)
            // }
        },
        createEdge(form) {
            var cx_from = this.from.firstChild.cx.baseVal.value;
            var cy_from = this.from.firstChild.cy.baseVal.value;
            var cx_to = this.to.firstChild.cx.baseVal.value;
            var cy_to = this.to.firstChild.cy.baseVal.value;
            var n = this.edges.filter((obj) => {
                    let cx_from_obj = obj.from.firstChild.cx.baseVal.value;
                    let cy_from_obj = obj.from.firstChild.cy.baseVal.value;
                    let cx_to_obj = obj.to.firstChild.cx.baseVal.value;
                    let cy_to_obj = obj.to.firstChild.cy.baseVal.value;
                    return (cx_from == cx_from_obj && cy_from == cy_from_obj && cx_to == cx_to_obj && cy_to == cy_to_obj) || (cx_to == cx_from_obj && cy_to == cy_from_obj && cx_from == cx_to_obj && cy_from == cy_to_obj);
                }).length;
            var res;
            var str = "";
            if (cx_from == cx_to && cy_from == cy_to) {
                res = this.createArrow_circle(cx_from,cy_from,n + 1);
            }
            else {
                var k = 30 / Math.sqrt(Math.pow(cx_to - cx_from,2) + Math.pow(cy_to - cy_from,2));
                var x1 = cx_from + k * (cx_to - cx_from);
                var y1 = cy_from + k * (cy_to - cy_from);
                var x2 = cx_to - k * (cx_to - cx_from);
                var y2 = cy_to - k * (cy_to - cy_from);
                res = this.createArrow(x1,y1,x2,y2,n + 1);
                var angle = Math.atan((cy_to - cy_from) / (cx_to - cx_from));
                str = "rotate(" + (angle * 180) / Math.PI  + " " + res[1] + " " + res[2]+ ")";
            }
            var oA = res[0];
            var x = res[1];
            var y = res[2];
            var oT_input = this.createTag("text",{"x":x - 20,"y":y - 10,"fill":"red","font-size":"20","text-anchor":"middle","transform":str});
            var oT_output = this.createTag("text",{"x":x + 20,"y":y - 10,"fill":"green","font-size":"20","text-anchor":"middle","transform":str});
            var oT_bracket = this.createTag("text",{"x":x,"y":y + 25,"fill":"white","font-size":"20","text-anchor":"middle","transform":str});
            oT_input.innerHTML = form.input;
            oT_output.innerHTML = form.output;
            var s = "";
            var s1 = "";
            for (let i in form.bracket_list) {
                if (form.bracket_list[i].bracket_type == "Open") {
                    switch (form.bracket_list[i].bracket_number) {
                        case "1":
                            s += "(";
                            s1 += "(";
                            break;
                        case "2":
                            s += "[";
                            s1 += "[";
                            break;
                        case "3":
                            s += "{";
                            s1 += "{";
                            break;
                        case "4":
                            s += "<";
                            s1 += "<";
                            break;
                        default:
                            s += ("(" + '<tspan style="baseline-shift:super;font-size:10;fill:white">' + form.bracket_list[i].bracket_number + "</tspan>");
                            s1 += ("(" + form.bracket_list[i].bracket_number);
                            break;
                    }
                }
                else if (form.bracket_list[i].bracket_type == "Close") {
                    switch (form.bracket_list[i].bracket_number) {
                        case "1":
                            s += ")";
                            s1 += ")";
                            break;
                        case "2":
                            s += "]";
                            s1 += "]";
                            break;
                        case "3":
                            s += "}";
                            s1 += "}";
                            break;
                        case "4":
                            s += ">";
                            s1 += ">";
                            break;
                        default:
                            s += (")" + '<tspan style="baseline-shift:super;font-size:10;fill:white">' + form.bracket_list[i].bracket_number + "</tspan>");
                            s1 += (")" + form.bracket_list[i].bracket_number);
                            break;
                    }
                }
                s += ('<tspan style="baseline-shift:sub;font-size:10;fill:white">' + form.bracket_list[i].bracket_label + "</tspan>");
                s1 += form.bracket_list[i].bracket_label;
            }
            oT_bracket.innerHTML = s;
            oA.appendChild(oT_input);
            oA.appendChild(oT_output);
            oA.appendChild(oT_bracket);
            this.container.appendChild(oA);
            this.edges.push({edge:oA,from:this.from,to:this.to});
            var vFrom = this.vertices_upload.filter((obj) => {
                    return this.from.lastChild.innerHTML == obj.id;
                });
            vFrom[0]["edges"].push({to:this.to.lastChild.innerHTML,input:form.input,output:form.output,bracket:s1});
            this.data_json.edges.push({from:this.from.lastChild.innerHTML, to:this.to.lastChild.innerHTML, form:JSON.stringify(form)});
            this.from = null;
            this.to = null;
        },
        createArrow(x1,y1,x2,y2,n) {
            var x0 = (x1 + x2) / 2;
            var y0 = (y1 + y2) / 2;
            var d = Math.sqrt(Math.pow(x2 - x1,2) + Math.pow(y2 - y1,2));
            var k = y1 == y2 ? Number.MAX_VALUE : (x1 - x2) / (y2 - y1);
            var x = d / (2 * Math.sqrt((Math.pow(k,2) + 1)));
            var y = k * x;
            var xn = x0 - Math.pow(-1,n) * parseInt(n / 2) * x;
            var yn = y0 - Math.pow(-1,n) * parseInt(n / 2) * y;
            var oG = this.createTag("g",{"onclick":"clickHandle_window(this)"});
			var oDefs = this.createTag("defs");
			var oMarker = this.createTag("marker",{"id":"triangle","markerUnits":"strokeWidth","markerWidth":"5","markerHeight":"4","refX":"4", "refY":"2","orient":"auto"});
			var oPath1 = this.createTag("path",{"d":"M 0 0 L 5 2 L 0 4 z", "fill":"white"});
			var oPath2 = this.createTag("path",{"d":"M " + x1 + " " + y1 + " Q " + xn + " " + yn + " " + x2 + " " + y2, "fill":"none", "stroke":"white", "stroke-width":"2", "style":"marker-end: url(#triangle);"});
			oMarker.appendChild(oPath1);
			oDefs.appendChild(oMarker);
			oG.appendChild(oDefs);
			oG.appendChild(oPath2);
			return [oG,(x0 + xn) / 2,(y0 + yn) / 2];
		},
        createArrow_circle(cx,cy,n) {
            var x1 = cx - 30;
            var y1 = cy;
            var x2 = cx + 30;
            var y2 = cy;
            var r = 30 + 20 * Math.ceil(n / 2);
            var oG = this.createTag("g",{"onclick":"clickHandle_window(this)"});
			var oDefs = this.createTag("defs");
			var oMarker = this.createTag("marker",{"id":"triangle","markerUnits":"strokeWidth","markerWidth":"5","markerHeight":"4","refX":"4", "refY":"2","orient":"auto"});
			var oPath1 = this.createTag("path",{"d":"M 0 0 L 5 2 L 0 4 z", "fill":"white"});
			var oPath2 = this.createTag("path",{"d":"M " + x1 + " " + y1 + " A " + r + " " + r + " 0 1 " + n % 2 + " " + x2 + " " + y2, "fill":"none", "stroke":"white", "stroke-width":"2", "style":"marker-end: url(#triangle);"});
			oMarker.appendChild(oPath1);
			oDefs.appendChild(oMarker);
			oG.appendChild(oDefs);
			oG.appendChild(oPath2);
            var y = (n % 2 == 1) ? cy - r - Math.sqrt(r * r - 900) : cy + r + Math.sqrt(r * r - 900);
			return [oG,cx,y];
        },
        setVertexType(type) {
            var curObj = this.vertices.filter((obj) => {
                    return this.selectedVertex == obj.vertex;
                });
            var vertex_upload = this.vertices_upload.filter((obj) => {
                    return this.selectedVertex.lastChild.innerHTML == obj.id;
                });
            var vertex_json = this.data_json.vertices.filter((obj) => {
                    return this.selectedVertex.lastChild.innerHTML == obj.id;
                });
            var curType = curObj[0].type;
            if (curType != type) {
                if (type == "Start") {
                    let temp = this.vertices.filter((obj) => {
                        return obj.type == "Start";
                    });
                    if (temp.length > 0) {
                        temp[0].vertex.removeChild(temp[0].vertex.childNodes[1]);
                        temp[0].vertex.firstChild.setAttribute("fill","aqua");
                        temp[0].type = "Normal";
                    }
                    if (curType == "End") {
                        this.selectedVertex.removeChild(this.selectedVertex.childNodes[1]);
                    }
                    this.selectedVertex.firstChild.setAttribute("fill","green");
                    let cx = this.selectedVertex.firstChild.cx.baseVal.value;
                    let cy = this.selectedVertex.firstChild.cy.baseVal.value;
                    let oA = this.createArrow(cx - 130,cy,cx - 30,cy,1)[0];
                    this.selectedVertex.insertBefore(oA, this.selectedVertex.lastChild);
                }
                else if (type == "Normal") {
                    this.selectedVertex.removeChild(this.selectedVertex.childNodes[1]);
                    this.selectedVertex.firstChild.setAttribute("fill","aqua");
                }
                else if (type == "End") {
                    if (curType == "Start") {
                        this.selectedVertex.removeChild(this.selectedVertex.childNodes[1]);
                    }
                    this.selectedVertex.firstChild.setAttribute("fill","red");
                    let cx = this.selectedVertex.firstChild.cx.baseVal.value;
                    let cy = this.selectedVertex.firstChild.cy.baseVal.value;
                    let oA = this.createArrow(cx + 30,cy,cx + 130,cy,1)[0];
                    this.selectedVertex.insertBefore(oA, this.selectedVertex.lastChild);
                }
                curObj[0].type = type;
                vertex_upload[0].type = type;
                vertex_json[0].type = type;
            }
            this.selectedVertex = null;
        },
        cancelHandle() {
            this.from = null;
            this.to = null;
        },
        confirmHandle(form) {
            this.createEdge(form);
        },
        cancelHandle_vertex() {
            this.selectedVertex = null;
        },
        confirmHandle_vertex(type) {
            this.setVertexType(type);
        },
        uploadData() {
            axios.post(this.path, this.vertices_upload)
                .then(() => {
                    this.downloadCode();
                })
                .catch((error) => {
                    console.log(error);
                });
        },
        downloadCode() {
            axios.get(this.path)
                .then((res) => {
                    let data = res.data;
                    const blob = new Blob([data])
                    let link = document.createElement('a')
                    link.href = window.URL.createObjectURL(blob)
                    link.download = 'result.py'
                    link.click()
                    this.$emit("statusChanged", 10);
                })
                .catch(error => {
                    console.error(error);
                });
        },
        downloadJSON() {
            let str = JSON.stringify(this.data_json);
            const blob = new Blob([str])
            let link = document.createElement('a')
            link.href = window.URL.createObjectURL(blob)
            link.download = 'l_graph.json'
            link.click()
            this.$emit("statusChanged", 11);
        },
        clear() {
            var first = this.container.firstChild
            while (first) {
                this.container.removeChild(first);
                first = this.container.firstChild;
            }
            this.vertexId = 0;
            this.from = null;
            this.to = null;
            this.vertices = [];
            this.edges = [];
            this.selectedVertex = null;
            this.vertices_upload = [];
            this.data_json = {vertices:[], edges:[]};
            this.$emit("statusChanged", 0);
        },
        uploadJSON() {
            this.fileReadDialogVisable = true;
            this.$emit("statusChanged", 0);
        },
        createFromJSON(str) {
            var obj = JSON.parse(str);
            this.clear();
            for (let i in obj.vertices) {
                this.createVertexWithCoordinate(obj.vertices[i].x, obj.vertices[i].y);
                this.selectedVertex = this.vertices.slice(-1)[0].vertex;
                this.setVertexType(obj.vertices[i].type);
            }
            for (let i in obj.edges) {
                this.from = this.vertices.filter(item => item.vertex.lastChild.innerHTML == obj.edges[i].from)[0].vertex;
                this.to = this.vertices.filter(item => item.vertex.lastChild.innerHTML == obj.edges[i].to)[0].vertex;
                this.createEdge(JSON.parse(obj.edges[i].form));
            }
        },
	},
	mounted() {
		this.initDom();
        window["clickHandle_window"] = (oG) => {
			this.clickHandle(oG);
		};
	},
	created() {},
    watch: {
        status: function (newStatus) {
            this.from = null;
            for (let i in this.vertices) {
                this.vertices[i].vertex.setAttribute("cursor","");
            }
            if (newStatus == 2 || newStatus == 3) {
                for (let i in this.vertices) {
                    this.vertices[i].vertex.setAttribute("cursor","pointer");
                }
            }
            if (newStatus == 4) {
                for (let i in this.vertices) {
                    this.vertices[i].vertex.setAttribute("cursor","pointer");
                }
                for (let i in this.edges) {
                    this.edges[i].edge.setAttribute("cursor","pointer");
                }
            }
            if (newStatus == 6) {
                this.clear();
            }
            if (newStatus == 7) {
                this.downloadJSON();
            }
            if (newStatus == 8) {
                this.uploadJSON();
            }
            if (newStatus == 9) {
                this.uploadData();
            }
        }
    },
};
</script>

<style scoped>
div {
    width: 80%;
    height: 75%;
    margin-left: 20%;
    margin-top: 0.5%;
    border-width: 1px;
    border-color: aqua;
    border-style: solid;
}
</style>