new Vue({
    el: '#random_exam',
    data: {
        words: null,
        answers: [],
        message: null,
        message_result: null,
        message_style: null,
        style_right: 'color: #5fc20a',
        style_fault: 'color: red',
    },
    mounted() {
        this.refresh()
    },
    methods: {
        refresh: function () {
            axios
                .get(location.origin + '/english_app/api/random_exam.json')
                .then(response => this.words = response.data.words)
                .catch(
                    function (error) {
                        console.log(error)
                    }
                );
            this.answers = [];
        },
        warning: function () {
            this.message = '请填写完整';
            this.message_result = null;
            this.message_style = this.style_fault;
        },
        submit: function () {
            console.log(this.answers);
            if (!(this.words.length === this.answers.length)) {
                this.warning()
                return
            }
            for (let index = 0; index < this.answers.length; index++) {
                console.log(this.answers[index])
                if (this.answers[index] === undefined) {
                    this.warning()
                    return
                } else if (!this.answers[index].trim()) {
                    this.warning()
                    return
                }
            }
            let that = this;
            axios
                .post(location.origin + '/english_app/api/random_exam.json',
                    {words: this.words, answers: this.answers,})
                .then(function (response) {
                    that.message_result = '\n已刷新题目';
                    that.message = response.data.msg + that.message_result;
                    if (response.data.status === 200) {
                        that.message_style = that.style_right
                    } else {
                        that.message_style = that.style_fault;
                    }
                })
                .catch(
                    function (error) {
                        console.log(error)
                    }
                );
            this.refresh()
        }
    },
});
