<template>
    <div class="container">
        <div class="search">
            <el-input v-model="input" placeholder="请输入汉字" width="100px" @input="inputHandle">
            </el-input>
            <el-button type="primary" icon="search" @click="searchHandle"></el-button>
        </div>
        <div class="pinyin">
            <div v-show="loading"><i class="el-icon-loading"></i></div>
            <ul v-for="wordMap in wordArr">
                <li>
                    <span class="title">{{ wordMap.word }}：</span>
                    <template v-for="yinpin in wordMap.yinpins">
                        <el-radio v-model="wordMap.radio" :label="yinpin" size="small">{{ yinpin }}</el-radio> 
                    </template>
                </li>
            </ul>
            <div class="conditions">
                <el-checkbox v-model="checked.start">开头</el-checkbox>
                <el-checkbox v-model="checked.end">结尾</el-checkbox>
                <el-checkbox v-show="checkedShow" v-model="checked.together">连续</el-checkbox>
            </div>
        </div>
        <div class="word-list">
            <ul>
                <li v-for="word in idealWords">{{ word.newWord }}({{word.originWord}})</li>
            </ul>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'Search',
        data() {
            return {
                wordArr: [
                    // {
                    //     word: '增',
                    //     yinpins: ['zeng', 'ceng'],
                    //     radio: ''
                    // },
                    // {
                    //     word: '长',
                    //     yinpins: ['zhang', 'chang'],
                    //     radio: ''
                    // }
                ],
                idealWords: [
                    // {
                    //     originWord: '',
                    //     newWord: ''
                    // }
                ],
                input: '',
                timer: '',
                loading: false,
                checked: {
                    together: false,
                    start: false,
                    end: false
                },
                checkedShow: false
            }
        },
        created() {

        },
        methods: {
            inputHandle() {
                let that = this;
                clearTimeout(this.timer);
                this.loading = true;
                // 检测是否存在非汉字
                if (this.input.match(/[\w\s].*/g)) {
                    return;
                }
                this.checkedShow = this.input.length > 1 ? true : false;
                this.timer = setTimeout(function(){
                    that.$http.get('/api/convert', {
                        params: {word: that.input}
                    }).then((res) => {
                        res = res.data;
                        if (res.status === true) {
                            that.wordArr = res.data;
                            that.loading = false;
                        }
                    }).catch((err) => {
                        console.log('err', err);
                    });
                }, 1000)
            },
            searchHandle() {
                let len = this.wordArr.length;
                if (len === 0) {
                    return;
                }
                for (let i = 0; i < len; i++) {
                    if (this.wordArr[i].radio === '') {
                        this.$message.error('请先选择拼音');
                        return;
                    }
                }
                this.$http.post('/api/search', {
                        data: this.wordArr
                    }).then((res) => {
                        res = res.data;
                        if (res.status === true) {
                            this.idealWords = res.data;
                        } else {
                            this.$message.error(res.msg);
                        }
                    }).catch((err) => {
                        console.log('err', err);
                    });
            }
        }
    }
</script>

<style>
    .container {
        width: 500px;
        position: absolute;
        left: 50%;
        margin-left: -250px;
    }
    .search div {
        width: 450px;
        float: left;
    }
    .search div input {
        border-bottom-right-radius: 0px;
        border-top-right-radius: 0px;
    }
    .search button {
        width: 50px;
        border-bottom-left-radius: 0px;
        border-top-left-radius: 0px;
    }
    .pinyin {
        text-align: left;
        margin-top: 10px;
    }
    .pinyin ul {
        margin: 0;
        padding: 0;
        list-style: none;
    }
    .yinpin ul li {
        margin: 0;
    }
    .conditions {
        margin-top: 10px;
    }
    .word-list ul {
        list-style: none;
        float: left;
        padding: 0;
    }
    .word-list ul li {
        float: left;
        padding: 5px;
        margin: 5px;
        color: #1D8CE0;
    }
</style>