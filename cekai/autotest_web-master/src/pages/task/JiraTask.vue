<template>
    <el-container>
        <el-header style="background: #fff; padding: 0; height: 50px">
            <div class="nav-api-header">
                <div style="padding-top: 10px; margin-left: 20px">
                    <el-button 
                    type="primary"
                     size="small"
                    icon="el-icon-circle-plus-outline"
                    @click="dialogVisible=true"
                    >
                    新增任务
                    </el-button>
                    <el-button 
                    v-show="taskData.count !== 0 "
                    style="margin-left: 20px"
                    type="danger"
                     size="small"
                    icon="el-icon-delete"
                    @click="delSelectionTasks"
                    >
                    批量删除
                    </el-button>

                    <el-dialog
                        title="添加任务"
                        :visible.sync="dialogVisible"
                        width="40%"
                        center
                    >
                        <el-form
                            :model="addtaskForm"
                            :rules="rules"
                            ref="addtaskForm"
                            label-width="150px"
                            class="project">
                            <el-form-item label="任务名称" prop="name">
                                <el-input v-model="addtaskForm.name" clearable placeholder="请输入任务名称"></el-input>
                            </el-form-item>       
                             <el-form-item label="JiraHost" prop="jirahost">
                                <el-input v-model="addtaskForm.jirahost" clearable placeholder="请输入jirahost"></el-input>
                            </el-form-item>     
                            <el-form-item label="JIRA查询语句" prop="jql">
                                <el-input v-model="addtaskForm.jql" clearable placeholder="请输入JIRA查询语句"></el-input>
                            </el-form-item>     
                            <el-form-item label="JIRABasicAuth" prop="BasicAuth">
                                <el-input v-model="addtaskForm.BasicAuth" clearable placeholder="请输入BasicAuth"></el-input>
                            </el-form-item>  
                            <el-form-item label="webhook" prop="webhook">
                                <el-input v-model="addtaskForm.webhook" clearable placeholder="请输入webhook"></el-input>
                            </el-form-item>   
                            <el-form-item label="时间设置" prop="crontab">
                                <el-input v-model="addtaskForm.crontab" clearable placeholder="请输入crontab"></el-input>
                            </el-form-item>  
                            <el-form-item label="搁置时长(天)" prop="expires_days">
                                <el-input v-model="addtaskForm.expires_days" clearable placeholder="请输入expires_days"></el-input>
                            </el-form-item>  
                             <el-form-item label="任务状态" prop="switch">
                            <el-switch v-model="addtaskForm.switch"></el-switch>
                            </el-form-item>
                            <el-form-item label="发送类型" prop="send_type">
                                <el-radio-group v-model="addtaskForm.send_type">
                                    <el-radio label="BUG提醒"></el-radio>
                                    <el-radio label="任务提醒"></el-radio>
                                    <el-radio label="品质部BUG提醒"></el-radio> 
                                    <el-radio label="品质部任务提醒"></el-radio>                                                               
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item label="项目测试人员" prop="tester">
                                <el-input v-model="addtaskForm.tester" clearable placeholder="请输入项目测试人员"></el-input>
                            </el-form-item>  
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="dialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleConfirm('addtaskForm')">确 定</el-button>
                      </span>
                    </el-dialog>  
                     <el-dialog
                        title="编辑任务"
                        :visible.sync="editdialogVisible"
                        width="40%"
                        center
                    >
                        <el-form
                            :model="edittaskFrom"
                            :rules="rules"
                            ref="edittaskFrom"
                            label-width="150px"
                            class="project">
                            <el-form-item label="任务名称" prop="name">
                                <el-input v-model="edittaskFrom.name" clearable placeholder="请输入任务名称"></el-input>
                            </el-form-item>     
                            <el-form-item label="JiraHost" prop="jirahost">
                                <el-input v-model="edittaskFrom.jirahost" clearable placeholder="请输入jirahost"></el-input>
                            </el-form-item>        
                            <el-form-item label="JIRA查询语句" prop="jql">
                                <el-input v-model="edittaskFrom.jql" clearable placeholder="请输入JIRA查询语句"></el-input>
                            </el-form-item>     
                            <el-form-item label="JIRABasicAuth" prop="BasicAuth">
                                <el-input v-model="edittaskFrom.BasicAuth" clearable placeholder="请输入BasicAuth"></el-input>
                            </el-form-item>  
                            <el-form-item label="webhook" prop="webhook">
                                <el-input v-model="edittaskFrom.webhook" clearable placeholder="请输入webhook"></el-input>
                            </el-form-item>   
                            <el-form-item label="时间设置" prop="crontab">
                                <el-input v-model="edittaskFrom.crontab" clearable placeholder="请输入crontab"></el-input>
                            </el-form-item>  
                            <el-form-item label="搁置时长(天)" prop="expires_days">
                                <el-input v-model="edittaskFrom.expires_days" clearable placeholder="请输入expires_days"></el-input>
                            </el-form-item>  
                             <el-form-item label="任务状态" prop="switch">
                            <el-switch v-model="edittaskFrom.switch"></el-switch>
                            </el-form-item>
                            <el-form-item label="发送类型" prop="send_type">
                                <el-radio-group v-model="edittaskFrom.send_type">
                                    <el-radio label="BUG提醒"></el-radio>
                                    <el-radio label="任务提醒"></el-radio>
                                    <el-radio label="品质部BUG提醒"></el-radio> 
                                     <el-radio label="品质部任务提醒"></el-radio>                          
                                </el-radio-group>
                            </el-form-item>
                            <el-form-item label="项目测试人员" prop="tester">
                                <el-input v-model="edittaskFrom.tester" clearable placeholder="请输入项目测试人员"></el-input>
                            </el-form-item>  
                        </el-form>
                        <span slot="footer" class="dialog-footer">
                        <el-button @click="editdialogVisible = false">取 消</el-button>
                        <el-button type="primary" @click="handleEditConfirm('edittaskFrom')">确 定</el-button>
                      </span>
                    </el-dialog>  
                </div>
            </div>
        </el-header>
        <el-container>
            <!-- <el-header style="padding: 0; height: 50px;">
                <div style="padding-top: 8px; padding-left: 20px; overflow: hidden;">
                    <el-row :gutter="50">
                        <el-col :span="6">
                            <el-input v-model="search" placeholder="请输入任务名称">
                                <el-button slot="append" icon="el-icon-search" @click="GetTaskList">
                                </el-button>
                            </el-input>
                        </el-col>
                    </el-row>
                </div>
            </el-header> -->
            <el-container>
                <el-main style="padding: 0; margin-left: 10px; margin-top: 10px;">
                    <div style="position: fixed; bottom: 0; right:0; left: 220px; top: 220px">
                           <el-table
                        :header-cell-style="{background:'#eef0f4',color:'#606266'}"
                            highlight-current-row
                            :data="taskData.results"
                            :show-header="taskData.results.length !== 0 "
                            stripe
                            height="calc(75%)"
                            @cell-mouse-enter="cellMouseEnter"
                            @cell-mouse-leave="cellMouseLeave"
                            @selection-change="handleSelectionChange"
                        >
                            <el-table-column
                                type="selection"
                                width="55"
                            >
                            </el-table-column>

                            <el-table-column
                                label="任务名称"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.name}}</div>
                                </template>
                            </el-table-column>

                            <el-table-column
                                label="时间设置"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.summary_kwargs.crontab}}</div>
                                </template>
                            </el-table-column>
                            <el-table-column
                                label="下次运行时间"
                            >
                                <template slot-scope="scope">
                                    <div>{{scope.row.summary_kwargs.next_run_time}}</div>
                                </template>
                            </el-table-column>
                        <el-table-column width="80" label="状态">
                            <template slot-scope="scope">
                                <el-switch
                                    disabled
                                    v-model="scope.row.enabled"
                                    active-color="#13ce66"
                                    inactive-color="#ff4949">
                                </el-switch>
                            </template>
                        </el-table-column>
                            <el-table-column
                            label="操作">
                                <template slot-scope="scope">
                                    <el-row v-show="currentRow === scope.row">
                                        <el-button
                                            type="info"                                           
                                            size="mini"
                                            @click="handerEdittask(scope.row)"
                                        >编辑</el-button>
                                        <el-button
                                            type="primary"                                           
                                            size="mini"
                                            @click="RunJIRASchedule(scope.row.id)"
                                        >运行</el-button>
                                        <el-button
                                            v-show="taskData.count !== 0"
                                            type="danger"                                  
                                            size="mini"
                                            @click="handerDelTask(scope.row.id)"
                                        >删除
                                        </el-button>
                                    </el-row>
                                </template>

                            </el-table-column>

                        </el-table>
                        <el-col :span="7">
                            <el-pagination
                                :page-size="11"
                                v-show="taskData.count !== 0 "
                                style="padding-top:10px;"
                                @current-change="handleCurrentChange"
                                :current-page.sync="currentPage"
                                layout="total, prev, pager, next, jumper"
                                :total="taskData.count"
                            >
                            </el-pagination>
                        </el-col>
                    </div>
                </el-main>
            </el-container>
        </el-container>
    </el-container>
</template>

<script>
import * as JiraTaskApi from '../../restful/jiratask' 
export default {

    data(){

        return{
            taskid:"",
            dialogVisible:false,
            editdialogVisible:false,
            search:'',
            currentRow:'',
            currentPage:1,
            selectVariables:[],
            data:[],
            taskData:{
                    count: 0,
                    results: []
            },
            addtaskForm:{
                name:'',
                jirahost:"",
                jql:"",
                BasicAuth:"",
                webhook:"",
                crontab:"",
                expires_days:3,
                switch:true,
                send_type:"BUG提醒",
                tester:""
            },
            edittaskFrom:{               
                name:'',
                 jirahost:"",
                jql:"",
                BasicAuth:"",
                webhook:"",
                crontab:"",
                expires_days:3,
                switch:true,
                send_type:"",
                tester:""
            },
            rules:{
                name: [
                        {required: true, message: '请输入任务名称', trigger: 'blur'},
                        {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ],
                jql: [
                        {required: true, message: '请输入JIRA查询语句', trigger: 'blur'},
                        {min: 1, max: 1000, message: '最多不超过1000个字符', trigger: 'blur'}
                    ],
                BasicAuth: [
                        {required: true, message: '请输入BasicAuth', trigger: 'blur'},
                        {min: 1, max: 1000, message: '最多不超过1000个字符', trigger: 'blur'}
                    ],
                webhook: [
                        {required: true, message: '请输入webhook', trigger: 'blur'},
                        {min: 1, max: 1000, message: '最多不超过100个字符', trigger: 'blur'}
                    ],
                crontab: [
                        {required: true, message: '请输入crontab', trigger: 'blur'},
                        {min: 1, max: 50, message: '最多不超过50个字符', trigger: 'blur'}
                    ],
                 jirahost:[
                        {required: true, message: '请输入jirahost', trigger: 'blur'},
                        {min: 1, max: 1000, message: '最多不超过1000个字符', trigger: 'blur'}
                    ],
                tester:[
                        {required: true, message: '请输入项目测试人员', trigger: 'blur'},
                        {min: 1, max: 100, message: '最多不超过100个字符', trigger: 'blur'}
                    ],
            }

        }

    },
    methods:{
        cellMouseEnter(row) {
                this.currentRow = row;
            },

        cellMouseLeave(row) {
                this.currentRow = '';
            },          
        
        handleSelectionChange(val) {
                this.selectVariables = val;
            },
        handleCurrentChange(val) {
                JiraTaskApi.getJiraTaskPaginationBypage({                    
                        page: this.currentPage,                     
                        search: this.search                  
                }).then(resp => {
                    this.taskData = resp;
                })
            },
           RunJIRASchedule(id){
                this.$confirm('此操作将运行此定时任务并发送企业微信, 是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning'
                }).then(() => {
                    this.loading = true;
                    JiraTaskApi.runJIRAScheduleTest({params:{taskid: id}}).then(resp => {
                        this.$notify.success('执行成功');
                        this.loading = false;
                    })
                    
                });
            },
        handleConfirm(fromName){
            this.$refs[fromName].validate((valid)=>{
                if(valid){
                    this.dialogVisible=false;
                    JiraTaskApi.AddJiratask(this.addtaskForm).then(resp =>{
                        if (resp.status === 201) {
                            this.$notify.success('添加定时任务成功');
                            this.GetTaskList();
                            this.$emit("changeStatus", false);
                        }
                            this.addtaskForm={
                                    name:'',
                                    jirahost:"",
                                    jql:"",
                                    BasicAuth:"",
                                    webhook:"",
                                    crontab:"",
                                    expires_days:3,
                                    switch:true,
                                    send_type:"BUG提醒",
                                    tester:""
                                }
                    })
                }
            })
        },

        delSelectionTasks() {
            if(this.selectVariables.length!==0){
                this.$confirm('此操作将永久删除勾选的任务，是否继续?', '提示',{
                        confirmButtonText: '确定',
                        cancelButtonText: '取消',
                        type: 'warning',
                }).then(()=>{
                    JiraTaskApi.DeleteAllJiraTask({data: this.selectVariables}).then(resp =>{
                            if (resp.status === 204){
                                this.$notify.success('批量删除定时任务成功');
                                this.GetTaskList();
                            }
                        

                    })
                })
            }

        },
        GetTaskList(){
            JiraTaskApi.GetJiratasklist().then(resp =>{
                console.log(resp)
               this.taskData=resp;
            })
        },

        handerEdittask(row){
            this.taskid=row.id
            this.edittaskFrom={             
                name: row.name,
                jirahost:row.summary_kwargs.jirahost,
                jql: row.summary_kwargs.jql,
                BasicAuth: row.summary_kwargs.BasicAuth,
                webhook:row.summary_kwargs.webhook,
                crontab:row.summary_kwargs.crontab,
                expires_days:row.summary_kwargs.expires_days,
                switch:row.summary_kwargs.switch,
                send_type:row.summary_kwargs.send_type,
                tester:row.summary_kwargs.tester
            };
            this.editdialogVisible=true;
        },
        handleEditConfirm(fromName){
            this.$refs[fromName].validate(valid=>{
                if(valid){
                    this.editdialogVisible=false;
                    JiraTaskApi.UpdateJiratask(this.taskid,this.edittaskFrom).then(resp =>{
                        if (resp.status === 201) {
                            this.$notify.success('修改定时任务成功');
                            this.$emit("changeStatus", false);
                            
                        }
                        this.GetTaskList();
                    })
                }
            })
        },
        handerDelTask(index){
            this.$confirm('此操作将永久删除该任务，是否继续?', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'warning',
                }).then(() => {
                    JiraTaskApi.DeleteJiratask(index).then(resp => {
                            if (resp.status === 204){
                                this.$notify.success('删除定时任务成功');
                                this.GetTaskList();
                            }
                     
                    })
                })
        }
        },
        name:'JiraTask',
        mounted(){
            this.GetTaskList();
          
        }
}

</script>