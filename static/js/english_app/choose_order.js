new Vue({
    el: '#choose_order',
    data: {
        now_order: '按最新',
        data_results: null
    },
    mounted() {
        // 请求数据
        this.get_words('/english_app/words.json');
    },
    methods: {
        get_words: function (url) {
            let full_url = location.origin + url;
            let that = this;
            axios
                .get(full_url)
                .then(function (response) {
                    that.data_results = response.data.results;
                    // console.log(response.data.results);
                })
                .catch(
                    function (error) {
                        console.log(error)
                    }
                )

        },
        new_order: function () {
            let my_order = '按最新';
            if (this.now_order !== my_order) {
                this.now_order = my_order;
                // 请求数据
                this.get_words('/english_app/words.json');
            }
        },
        word_abc_order: function () {
            let my_order = '按字母顺序';
            if (this.now_order !== my_order) {
                this.now_order = my_order;
                // 请求数据
                this.get_words('/english_app/words.json?ordering=english');
            }
        },
        error_rate_order: function () {
            let my_order = '按错误率';
            if (this.now_order !== my_order) {
                this.now_order = my_order;
                // 请求数据
                this.get_words('/english_app/words.json?ordering=error');
            }
        },

    },
});