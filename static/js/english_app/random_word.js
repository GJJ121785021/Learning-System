new Vue({
    el: '#random_word',
    data: {
        in_result: null,
        into_english: null,
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
                .get(location.origin + '/english_app/api/random_word/?format=json')
                .then(response => this.into_english = response.data.english)
                .catch(
                    function (error) {
                        console.log(error)
                    }
                );
            this.in_result = null;
        },
        submit: function () {
            if (!this.in_result){
                this.message = '请输入你的翻译结果';
                this.message_result = null;
                this.message_style = this.style_fault;
                return
            }
            let that = this;
            axios
                .post(location.origin + '/english_app/api/random_word/',
                    {english: this.into_english, chinese_translation: this.in_result,})
                .then(function (response) {
                    that.message = response.data.msg + '-> ' + response.data.english;
                    that.message_result = response.data.chinese_translation;
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
