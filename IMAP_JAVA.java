import java.io.File;
import java.io.FileOutputStream;
import java.util.Properties;

import javax.mail.Address;
import javax.mail.BodyPart;
import javax.mail.Folder;
import javax.mail.Message;
import javax.mail.Multipart;
import javax.mail.Session;
import javax.mail.Store;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeBodyPart;
import javax.mail.internet.MimeMultipart;

public class EmailDownloader {

    public static void main(String[] args) throws Exception {
        // Ask for email and password
        String email = System.console().readLine("Email: ");
        char[] password = System.console().readPassword("Password: ");

        // Set mail properties
        Properties props = new Properties();
        props.put("mail.store.protocol", "imaps");
        props.put("mail.imap.host", "imap.gmail.com");
        props.put("mail.imap.port", "993");
        props.put("mail.imap.ssl.enable", "true");

        // Connect to mail server
        Session session = Session.getDefaultInstance(props, null);
        Store store = session.getStore("imaps");
        store.connect("imap.gmail.com", email, new String(password));

        // Open inbox folder
        Folder inbox = store.getFolder("INBOX");
        inbox.open(Folder.READ_ONLY);

        // Get last 100 messages
        Message[] messages = inbox.getMessages(inbox.getMessageCount() - 99, inbox.getMessageCount());

        // Create directory for messages
        File messageDir = new File("email_messages");
        messageDir.mkdir();

        // Loop over messages and download attachments
        for (Message message : messages) {
            String subject = message.getSubject();
            Address[] from = message.getFrom();
            String fromEmail = ((InternetAddress) from[0]).getAddress();

            // Download attachments
            Object content = message.getContent();
            if (content instanceof Multipart) {
                Multipart multipart = (Multipart) content;
                for (int i = 0; i < multipart.getCount(); i++) {
                    BodyPart bodyPart = multipart.getBodyPart(i);
                    if (bodyPart.getFileName() != null) {
                        String fileName = bodyPart.getFileName();
                        File file = new File(messageDir, fileName);
                        FileOutputStream fos = new FileOutputStream(file);
                        MimeBodyPart mimeBodyPart = (MimeBodyPart) bodyPart;
                        mimeBodyPart.getDataHandler().writeTo(fos);
                        fos.close();
                    }
                }
            }
        }

        // Close folder and store
        inbox.close(false);
        store.close();
    }

}
