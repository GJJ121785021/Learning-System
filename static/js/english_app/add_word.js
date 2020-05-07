new Vue({
    el: '#add_word',
    data: {
        in_word: null,
        message: null,
        message_style: null,
        word_success: '添加成功',
        word_exist: '单词已存在',
        word_empty: '请输入单词',
        word_error: '请输入正确的单词',
        style_success: 'color: #5fc20a',
        style_exist: 'color: red',
    },
    methods: {
        get_csrf_token: function () {
            return document.getElementById("my_csrf").getElementsByTagName("input")[1].value
        },
        to_url: function () {
            return location.origin + '/english_app/words/'
        },
        before_submit: function () {
            // let reg = /^[A-Za-z]+$/;
            if (!this.in_word) {
                this.message = this.word_empty;
                this.message_style = this.style_exist;
                return true
            } else if (!/^[A-Za-z]+$/.test(this.in_word.trim())) {
                this.message = this.word_error;
                this.message_style = this.style_exist;
                return true
            }
        },
        add_into_it: function () {
            if (this.before_submit()) {
                return
            }
            let that = this;
            axios
                .post(this.to_url(), {english: this.in_word, csrfmiddlewaretoken: this.get_csrf_token()})
                .then(function (response) {
                    console.log(response.data);
                    location.href = response.data.url
                })
                .catch(
                    function () {
                        that.message = that.word_exist;
                        that.message_style = that.style_exist;
                    }
                )
        },
        add_once_again: function () {
            if (this.before_submit()) {
                return
            }
            let that = this;
            axios
                .post(this.to_url(), {english: this.in_word, csrfmiddlewaretoken: this.get_csrf_token()})
                .then(function () {
                    that.message = that.word_success;
                    that.message_style = that.style_success;
                })
                .catch(
                    function () {
                        that.message = that.word_exist;
                        that.message_style = that.style_exist;
                    }
                )
        },

    }
})