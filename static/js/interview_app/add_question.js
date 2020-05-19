new Vue({
    el: '#add_interview',
    data: {
        in_question: null,
        in_answer: null,
        message: null,
        message_style: null,
        add_success: '添加成功',
        add_exist: '题目已存在',
        question_empty: '请输入题目',
        answer_empty: '请输入答案',
        style_success: 'color: #5fc20a',
        style_exist: 'color: red',
    },
    methods: {
        to_url: function () {
            return location.origin + '/interview_app/api/interview_questions/'
        },
        before_submit: function () {
            // let reg = /^[A-Za-z]+$/;
            if (!this.in_question) {
                this.message = this.question_empty;
                this.message_style = this.style_exist;
                return true
            }
            if (!this.in_answer) {
                this.message = this.answer_empty;
                this.message_style = this.style_exist;
                return true
            }
        },
        add_once_again: function () {
            // console.log(this.in_question);
            if (this.before_submit()) {
                return
            }
            let that = this;
            axios
                .post(this.to_url(), {question: this.in_question, answer: this.in_answer })
                .then(function (response) {
                    that.message = that.add_success + '--->' + that.in_question;
                    that.message_style = that.style_success;
                })
                .catch(
                    function () {
                        that.message = that.add_exist;
                        that.message_style = that.style_exist;
                    }
                )
        },

    }
})