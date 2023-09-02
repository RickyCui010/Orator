package com.ricky;//import com.sun.istack.internal.NotNull;
import javax.validation.constraints.Max;
import org.apache.log4j.Logger;
import org.java_websocket.client.WebSocketClient;
import org.java_websocket.enums.ReadyState;
import org.java_websocket.handshake.ServerHandshake;
import org.json.JSONException;
import org.json.JSONObject;

import java.net.URI;
import java.net.URISyntaxException;

/*
*这个程序使用org.java_websocket库来与ROS Bridge服务器通信，并通过WebSocket协议订阅并发送指令。在这个示例中，
*程序能够订阅名为/cmd_vel的ROS主题，并发送机器人运动控制消息到该主题。
* 机器人可以按照方向和距离参数行走到需要的位置
* @Author sjc
*/
public class RobotControlClient {
    private static final String ROSBRIDGE_SERVER_URL = "ws://10.251.178.142:9090";
    private static WebSocketClient rosBridgeClient;


    public static void main(String[] args) {
        initRosBridgeClient();
        //有间隔的多次发送数据，实现长距离直线行走。其他方向类似。
        //todo 目前由于机器人关于这方面的消息接受似乎有限制，循环过多会导致进程被杀，分析改进中
        int i = 0;
        while (i < 1){
            moveRobot(0.17, 0.0, 0.0, 0.0);//向前移动
            delay(300);//停滞
            System.out.println(i);
            i++;
        }
        stopRobot();
//        closeRosBridgeClient();
    }

    private static void initRosBridgeClient() {
        try {
            rosBridgeClient = new WebSocketClient(new URI(ROSBRIDGE_SERVER_URL)) {
                @Override
                public void onOpen(ServerHandshake serverHandshake) {
                    System.out.println("[INFO] Connected to ROSBridge server.");
                }

                @Override
                public void onMessage(String s) {
                }

                @Override
                public void onClose(int i, String s, boolean b) {
                    System.out.println("[INFO] Disconnected ROSBridge server ");
                }

                @Override
                public void onError(Exception e) {
                    System.out.println("[ERROR] Failed ROSBridge server.");
                    e.printStackTrace();
                }
            };
            rosBridgeClient.connect();
        } catch (URISyntaxException e) {
            System.out.println("[ERROR]  ROSBridge server URL 错误.");
            e.printStackTrace();
        }
    }

    private static void closeRosBridgeClient() {
        try {
            rosBridgeClient.closeBlocking();
        } catch (InterruptedException e) {
            System.out.println("[ERROR] An error occurred while closing the ROSBridge client.");
            e.printStackTrace();
        }
    }

    //该方法控制机器人移动。前三个参数确定平面移动方向，第四个参数控制机器人原地旋转。
    private static void moveRobot(double l_x, double l_y, double l_z,  double a_z) {
        Logger logger = Logger.getLogger("RobotControlClient");
        JSONObject msg = new JSONObject();
        try {
            msg.put("op", "publish");
            msg.put("topic", "/cmd_vel");
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JSONObject twist = new JSONObject();
        JSONObject linear = new JSONObject();
        try {
            linear.put("x", l_x);
            linear.put("y", l_y);
            linear.put("z", l_z);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        JSONObject angular = new JSONObject();
        //默认角速度为零，不转弯
        try {
            angular.put("x", 0.0);
            angular.put("y", 0.0);
            angular.put("z", a_z);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        try {
            twist.put("linear", linear);
            twist.put("angular", angular);
            msg.put("msg", twist);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        logger.info("###########");

        //这里需要确定websocket连接成功之后再发送数据
        while(!(ReadyState.OPEN).equals(rosBridgeClient.getReadyState())){
            logger.info("socket连接还未打开");
        }
        rosBridgeClient.send(msg.toString());

    }

    private static void stopRobot() {
        moveRobot(0.0, 0.0, 0.0, 0.0);
    }

    private static void delay(int milliseconds) {
        try {
            Thread.sleep(milliseconds);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }


    //todo
    // moveRobot_Sum方法包含住moveRobot方法，该方法可以实现机器人前后左右移动，360度旋转，但不能同时实现两个方向的移动。
    // 传递的参数例子如下：
    // moveRobot_Sum(方向参数：turn 1-前、2-后、3-左、4-右, 平面距离：10 >= dis_sum >= 0 单位 米 , 旋转角度：360 >=ang_sum >= 0 )
    // dis_sum和 ang_sum必须有一个是0，且dis_sum距离不能过大，会导致进程崩溃。
    public static String moveRobot_Sum( int turn, @Max(10) int dis_sum, @Max(360) int ang_sum){
        initRosBridgeClient();
        if (ang_sum != 0 && dis_sum == 0){
            int J = (int)Math.ceil((double)ang_sum / 3.6);//J是计算后循环发送的次数（旋转度数）
            int j = 0;
            while (j < J){
                moveRobot(0.0, 0.0, 0.0, 0.422);//旋转
                delay(200);//停滞
                j++;
            }
            stopRobot();
            return "旋转了"+ang_sum+"度";
        } else if (ang_sum == 0 && dis_sum != 0){
            switch (turn)
            {
                case 1: //向前走
                    //取整，距离大致相同
                    int W = (int)Math.ceil((double)dis_sum / 0.023);//I是计算后循环发送的次数（平面距离）
                    int w = 0;
                    while (w < W){
                        moveRobot(0.17, 0.0, 0.0, 0.0);//向前移动 以0.17的速度，一条消息前进3.8厘米
                        delay(300);//停滞
                        w++;
                    }
                    //行进一段路程之后内置停止行进方法
                    stopRobot();
                    return "向前移动"+dis_sum+"米";
                case 2: //向后走
                    int bac = 0;
                    while (bac < 50){
                        moveRobot(0.0, 0.0, 0.0, 0.422);//向前移动
                        delay(200);//停滞
//                        System.out.println(bac);
                        bac++;
                    }
                    int S = (int)Math.ceil((double)dis_sum / 0.023);//I是计算后循环发送的次数（平面距离）
                    int s = 0;
                    while (s < S){
                        moveRobot(0.17, 0.0, 0.0, 0.0);//向后移动
                        delay(300);//停滞
                        s++;
                    }
                    stopRobot();
                    return "向后移动"+dis_sum+"米";
                case 3: //向左走
                    int A = (int)Math.ceil((double)dis_sum / 0.023);//I是计算后循环发送的次数（平面距离）
                    int a = 0;
                    while (a < A){
                        moveRobot(0.0, 0.17, 0.0, 0.0);//向左移动
                        delay(300);//停滞
                        a++;
                    }
                    stopRobot();
                    return "向左移动"+dis_sum+"米";
                default://向右走
                    int D = (int)Math.ceil((double)dis_sum / 0.023);//I是计算后循环发送的次数（平面距离）
                    int d = 0;
                    while (d < D){
                        moveRobot(0.0, -0.17, 0.0, 0.0);//向右移动
                        delay(300);//停滞
                        d++;
                    }
                    stopRobot();
                    return "向右移动"+dis_sum+"米";
            }
        }else {
            return "传入参数内容不正确";
        }

    }
}
