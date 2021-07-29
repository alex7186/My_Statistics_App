import java.awt.*;
import java.awt.geom.AffineTransform;
import java.awt.image.AffineTransformOp;
import java.awt.image.BufferedImage;
import java.io.*;
import java.net.*;
import java.util.Arrays;

import org.json.JSONObject;
import org.json.JSONArray;
import javax.imageio.ImageIO;
import javax.swing.*;

public class main {
    public static void main(String[] args) throws IOException {

        // server ip and port
        String address = "http://192.168.0.125:5001";
        // type of analysis ("1_arr" or "2_arr")
        String type = "1_arr";
        // parameters of content of server answer
        String[] needed_params = {"make_text", "make_hist", "make_boxplot"};

        // arr to analise
        double[] arr = {42.0, 42.5, 41.9, 41.5, 41.8};
        // extra arr to analise
        // used if type of analysis String type = "2_arr";
        double[] arr2 = {41, 41.2, 41.3};

        // relative dispersion of applied analysis method
        // leave it in -100 if you dont have such
        double sr_meth = -100;
        // true correct value for array of your data
        // leave it in -100 if you dont have such
        double true_value = -100;


        // make JSONArray of server answer content as a result of sending post request
        JSONArray res_array = new JSONArray(String.valueOf(
                executePost(address, generate_params(arr, arr2, sr_meth, true_value, needed_params, type))
        ));

        // show all JSONObjects from JSONArray in separated JFrames
        show_res_array(res_array);

    }

    static String generate_params(double[] arr1, double[] arr2, double sr_met, double true_value, String[] needed_params, String type){
        // check if involved parameters are allowed to send
        String[] req_params_1_arr = {"make_text", "make_hist", "make_boxplot"};
        String[] req_params_2_arr = {"make_text", "make_boxplot"};

        String[] curr_req_params = new String[0];
        String postfix = "";
        StringBuilder param_sum = new StringBuilder();
        if (type.equals("2_arr")) {
            curr_req_params = req_params_2_arr;
            postfix = ",\"req_type\": \"2_arr\"}";
            param_sum = new StringBuilder("{\"arr1\": " + arr_to_python_str(arr1) + ", \"arr2\": " + arr_to_python_str(arr2) + ",");
        }
        else if (type.equals("1_arr")){
            curr_req_params = req_params_1_arr;
            postfix = ",\"req_type\": \"1_arr\"}";

            postfix = ",\"sr_met\":" + sr_met + postfix;
            postfix = ",\"true_value\":" + true_value + postfix;

            param_sum = new StringBuilder("{\"arr_data\": " + arr_to_python_str(arr1) + ",");
        }

        // converting all parameters to the completed string
        for (String prm: curr_req_params){
            String str;
            if (Arrays.asList(needed_params).contains(prm)){
                str = "\"" + prm + "\":1,";
            }
            else {
                str = "\"" + prm + "\":0,";
            }
            param_sum.append(str);
        }
        param_sum = new StringBuilder(param_sum.substring(0, param_sum.length() - 1));
        return param_sum + postfix;
    }

    static String arr_to_python_str(double[] arr){
        // converting arr to the parameter for post request
        StringBuilder sum = new StringBuilder("[");
        for (double v : arr) {
            sum.append(v).append(", ");
        }
        return sum.substring(0, sum.length()-2) + "]";
    }

    static void show_res_array(JSONArray res_array) throws IOException {

        int i_w = 580;
        int i_h = 350;
        int t_w = 500;
        int t_h = 700;

        int summary_bias = 0;
        int bias_right = 300;

        double scale = 0.65;


        for (int i = 0; i < res_array.length(); i++) {

            // JPanel is created for each JSONObject
            JSONObject row = (JSONObject) res_array.get(i);
            String row_type = (String) row.get("type");
            String row_content = (String) row.get("content");

            if (row_content.length() > 0) {

                if (row_type.equals("image")) {
                    BufferedImage img = B64_to_BI(row_content, scale);
                    JFrame frame = new JFrame();
                    frame.setSize(i_w, i_h);
                    JPanel pane = panel_from_image(img);
                    frame.add(pane);
                    frame.setLocation(summary_bias, 0);
                    summary_bias += bias_right;
                    frame.setVisible(true);

                }
                if (row_type.equals("text")){
                    JFrame frame = new JFrame();
                    frame.setSize(t_w, t_h);
                    frame.setLayout(new GridBagLayout());
                    JLabel jlabel = new JLabel();
                    // a bit of text formatting with html tags
                    jlabel.setText(
                            "<html>" +
                                    row_content.replace(
                                            "\n", "<br>"
                                    ).replace(
                                            "\t", "&nbsp;&nbsp;&nbsp;"
                                    ) +
                                    "<html/>");

                    JPanel panel = new JPanel();
                    panel.add(jlabel);
                    frame.add(panel, new GridBagConstraints());
                    frame.setLocation(summary_bias, 0);
                    summary_bias += bias_right;
                    frame.setVisible(true);
                }
            }
        }
    }

    static JPanel panel_from_image(BufferedImage img){
        // returns JPanel with image involved
        return new JPanel() {
            @Override
            protected void paintComponent(Graphics g) {
                super.paintComponent(g);
                g.drawImage(img, 0, 0, null);
            }
        };
    }

    static BufferedImage B64_to_BI(String png_text, double scale) throws IOException {
        // make BufferedImage from base64 string
        byte[] imageBytes = javax.xml.bind.DatatypeConverter.parseBase64Binary(png_text);
        BufferedImage img = ImageIO.read(new ByteArrayInputStream(imageBytes));

        int w = img.getWidth();
        int h = img.getHeight();

        // smoothly scaling the image
        BufferedImage after = new BufferedImage(w, h, BufferedImage.TYPE_INT_ARGB);
        AffineTransform at = new AffineTransform();
        at.scale(scale, scale);
        AffineTransformOp scaleOp =
                new AffineTransformOp(at, AffineTransformOp.TYPE_BILINEAR);
        after = scaleOp.filter(img, after);
        return after;
    }

    static String executePost(String address, String urlParameters) {
        HttpURLConnection connection = null;

        try {
            //Create connection
            URL url = new URL(address);
            connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setRequestProperty("Content-Type",
                    "application/x-www-form-urlencoded");

            connection.setRequestProperty("Content-Length",
                    Integer.toString(urlParameters.getBytes().length));
            connection.setRequestProperty("Content-Language", "en-US");

            connection.setUseCaches(false);
            connection.setDoOutput(true);

            //Send request
            DataOutputStream wr = new DataOutputStream (
                    connection.getOutputStream());
            wr.writeBytes(urlParameters);
            wr.close();

            //Get Response
            InputStream is = connection.getInputStream();
            BufferedReader rd = new BufferedReader(new InputStreamReader(is));
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = rd.readLine()) != null) {
                response.append(line);
                response.append('\r');
            }
            rd.close();
            return response.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}

