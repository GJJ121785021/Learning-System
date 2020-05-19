new Vue({
    el: '#interview_index',
    data: {
        data: {results: null},
        now_page: 1,
        previous_button: 'page-item disabled',
        next_button: 'page-item',
    },
    mounted() {
        this.get_interview_questions('/interview_app/api/interview_questions.json')
    },
    methods: {
        get_interview_questions: function (url, into_full_url = null) {
            if (into_full_url) {
                full_url = into_full_url
            } else {
                full_url = location.origin + url;
            }
            let that = this;
            axios
                .get(full_url)
                .then(function (response) {
                    that.data = response.data;
                    // console.log(response.data.results);
                    // 检查上下页按钮的有效性
                    if (response.data.previous) {
                        that.previous_button = 'page-item'
                    } else {
                        that.previous_button = 'page-item disabled'
                    }
                    if (response.data.next) {
                        that.next_button = 'page-item'
                    } else {
                        that.next_button = 'page-item disabled'
                    }
                })
                .catch(
                    function (error) {
                        console.log(error)
                    }
                )
        },
        // 上一页
        previous_page: function () {
            if (this.data.previous) {
                this.get_words(null, this.data.previous);
                this.now_page--;

            }
        },
        // 下一页
        next_page: function () {
            if (this.data.next) {
                this.get_words(null, this.data.next);
                this.now_page++;
            }


        },
    },
})
