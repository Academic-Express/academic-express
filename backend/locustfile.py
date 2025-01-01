from locust import HttpUser, TaskSet, between, task


class UserBehavior(TaskSet):
    def on_start(self):
        """在测试开始时登录用户"""
        self.login()

    def login(self):
        response = self.client.post("/api/v1/user/login", json={
            "username": "test",
            "password": "test"
        })
        if response.status_code == 200:
            self.token = response.json().get("access")
            self.client.headers.update(
                {"Authorization": f"Bearer {self.token}"})
        else:
            self.token = None
            print(f"Login failed: {response.status_code} {response.text}")

    @task(1)
    def get_user_profile(self):
        """获取用户个人资料"""
        if self.token:
            self.client.get("/api/v1/user/profile")

    @task(2)
    def view_collections(self):
        """查看用户收藏"""
        if self.token:
            self.client.get("/api/v1/collections/")

    @task(3)
    def post_comment(self):
        """发表评论并获取评论 ID"""
        if self.token:
            response = self.client.post("/api/v1/comments/resource/", json={
                "content": "This is a test comment."
            })
            if response.status_code == 201:
                comment_id = response.json().get("id")
                self.client.get(f"/api/v1/comments/{comment_id}")
            else:
                print(f"Post comment failed: {response.status_code} {response.text}")

    @task(4)
    def view_hot_feed(self):
        """查看热门内容"""
        self.client.get("/api/v1/feed/hot")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)  # 模拟用户在请求之间的思考时间
