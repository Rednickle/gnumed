/*
 * TestReferralPanel.java
 *
 * Created on 22 August 2003, 22:14
 */

package quickmed.usecases.test;
import org.gnumed.gmIdentity.identity;
import java.text.*;
import java.util.*;import java.util.logging.*;

import java.io.*;
import gnmed.test.DomainPrinter;
import javax.print.*;
import javax.print.attribute.*;
import javax.print.attribute.standard.*;
import javax.swing.*;
/**
 *
 * @author  sjtan
 */
public class TestReferralPanel extends javax.swing.JPanel implements ClientProviderRelatable {
//    public static final int DEFAULT_PLAINTEXT_LINELEN= 56;
//    public static final int DEFAULT_PLAINTEXT_TABSIZE = 8;
//    public static final int HACKY_LEFT_MARGIN = 4;
//    
    
    private BasicLetterGenerationCapable generator = new PlainLetterBasicGenerator();
    private ContactsPanel contacts;
    private identity client;
    /** Creates new form TestReferralPanel */
    public TestReferralPanel() {
        initComponents();
        addContactsPanel();
        changeTabNames();
        //        addPrintServiceUI();
   
        addProviderSelectionListener();
    }
    
    void addContactsPanel() {
        contacts = new ContactsPanel();
        jPanel5.add(contacts);
        validate();
    }
    
    //    void  addPrintServiceUI() {
    //        PrintService service = PrintServiceLookup.lookupDefaultPrintService();
    //        ServiceUIFactory factory = service.getServiceUIFactory();
    //
    //        ServiceUI ui = factory.getUI( factory.MAIN_UIROLE, factory.JCOMPONENT_UI);
    //        jTabbedPane1.addTab(Globals.bundle.getString("print_setup"), ui);
    //    }
    
    void changeTabNames() {
        jTabbedPane1.setTitleAt(0, Globals.bundle.getString("select_contact"));
        jTabbedPane1.setTitleAt(1, Globals.bundle.getString("letter"));
        
    }
    
    class ProviderSelectionGenerateLetterListener implements java.beans.PropertyChangeListener {
        
        public void propertyChange(java.beans.PropertyChangeEvent evt) {
            if (evt.getPropertyName().equals("providerSelected") &&
            evt.getNewValue() != null && evt.getNewValue().equals( new Boolean(true) ) )
                try {
            generateReferralFile();
                } catch (Exception e) {
                    e.printStackTrace();
                }
        }        
        
    }
    
    void addProviderSelectionListener() {
        contacts.addPropertyChangeListener(
        new ProviderSelectionGenerateLetterListener() 
        );
    }
    /** This method is called from within the constructor to
     * initialize the form.
     * WARNING: Do NOT modify this code. The content of this method is
     * always regenerated by the Form Editor.
     */
    private void initComponents() {//GEN-BEGIN:initComponents
        java.awt.GridBagConstraints gridBagConstraints;

        jTabbedPane1 = new javax.swing.JTabbedPane();
        jPanel3 = new javax.swing.JPanel();
        jScrollPane1 = new javax.swing.JScrollPane();
        jPanel5 = new javax.swing.JPanel();
        jPanel4 = new javax.swing.JPanel();
        jScrollPane2 = new javax.swing.JScrollPane();
        jEditorPane1 = new javax.swing.JEditorPane();
        jPanel6 = new javax.swing.JPanel();
        printButton2 = new javax.swing.JButton();
        saveButton = new javax.swing.JButton();
        jPanel2 = new javax.swing.JPanel();
        generateLetterButton = new javax.swing.JButton();
        jPanel1 = new javax.swing.JPanel();
        jLabel1 = new javax.swing.JLabel();
        jTextField1 = new javax.swing.JTextField();
        jButton1 = new javax.swing.JButton();

        setLayout(new java.awt.GridBagLayout());

        jPanel3.setLayout(new java.awt.BorderLayout());

        jPanel5.setLayout(new javax.swing.BoxLayout(jPanel5, javax.swing.BoxLayout.X_AXIS));

        jScrollPane1.setViewportView(jPanel5);

        jPanel3.add(jScrollPane1, java.awt.BorderLayout.CENTER);

        jTabbedPane1.addTab("tab1", jPanel3);

        jPanel4.setLayout(new java.awt.BorderLayout());

        jScrollPane2.setViewportView(jEditorPane1);

        jPanel4.add(jScrollPane2, java.awt.BorderLayout.CENTER);

        printButton2.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("print"));
        printButton2.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                printButton2ActionPerformed(evt);
            }
        });

        jPanel6.add(printButton2);

        saveButton.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("save"));
        jPanel6.add(saveButton);

        jPanel4.add(jPanel6, java.awt.BorderLayout.SOUTH);

        jTabbedPane1.addTab("tab2", jPanel4);

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridwidth = java.awt.GridBagConstraints.REMAINDER;
        gridBagConstraints.fill = java.awt.GridBagConstraints.BOTH;
        gridBagConstraints.weightx = 4.0;
        gridBagConstraints.weighty = 4.0;
        add(jTabbedPane1, gridBagConstraints);

        generateLetterButton.setMnemonic(java.util.ResourceBundle.getBundle("SummaryTerms").getString("generate_letter").charAt(0));
        generateLetterButton.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("generate_letter"));
        generateLetterButton.addActionListener(new java.awt.event.ActionListener() {
            public void actionPerformed(java.awt.event.ActionEvent evt) {
                generateLetterButtonActionPerformed(evt);
            }
        });

        jPanel2.add(generateLetterButton);

        add(jPanel2, new java.awt.GridBagConstraints());

        jPanel1.setLayout(new java.awt.GridBagLayout());

        jLabel1.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("editor_app"));
        jLabel1.setFocusable(false);
        jLabel1.setEnabled(false);
        jPanel1.add(jLabel1, new java.awt.GridBagConstraints());

        jTextField1.setText("jTextField1");
        jTextField1.setFocusable(false);
        jTextField1.setEnabled(false);
        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        jPanel1.add(jTextField1, gridBagConstraints);

        jButton1.setText(java.util.ResourceBundle.getBundle("SummaryTerms").getString("set_editor"));
        jButton1.setFocusable(false);
        jButton1.setEnabled(false);
        jPanel1.add(jButton1, new java.awt.GridBagConstraints());

        gridBagConstraints = new java.awt.GridBagConstraints();
        gridBagConstraints.gridwidth = java.awt.GridBagConstraints.REMAINDER;
        gridBagConstraints.fill = java.awt.GridBagConstraints.HORIZONTAL;
        gridBagConstraints.weightx = 1.0;
        add(jPanel1, gridBagConstraints);

    }//GEN-END:initComponents
    
    private void printButton2ActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_printButton2ActionPerformed
        // Add your handling code here:
        
        //        PrintService service =  PrintServiceLookup.lookupDefaultPrintService();
        //        PrintRequestAttributeSet aset = new HashPrintRequestHashAttributeSet();
        //         aset.add(MediaSizeName.ISO_A4);
        //        DocPrintJob job = service.createPrintJob();
        //        job.
        
        int x =  ((java.awt.Component)evt.getSource()).getX();
        int y =  ((java.awt.Component)evt.getSource()).getY();
        
        DocFlavor flavor = DocFlavor.INPUT_STREAM.AUTOSENSE;
        
        
        HashPrintRequestAttributeSet attributes = new HashPrintRequestAttributeSet();
        attributes.add( MediaSizeName.ISO_A4);
        attributes.add( MediaSizeName.FOLIO);
        
        
        
        PrintService[] services = PrintServiceLookup.lookupPrintServices(flavor, attributes);
        if (services == null || services.length == 0) {
            services = new PrintService[] { PrintServiceLookup.lookupDefaultPrintService() };
            
        }
        for (int j = 0; j < services.length; ++j) {
            System.out.println("SERVICE = " + services[j].getName() );
            DocFlavor [] supported = services[j].getSupportedDocFlavors();
            for (int i = 0; i < supported.length; ++i) {
                System.out.println("SUPPORTED FLAVORS = " +
                supported[i].hostEncoding + ",  "+
                supported[i].getClass().getName() + " , " +
                supported[i].getRepresentationClassName() );
            }
        }
        
        
        
        PrintService service = ServiceUI.printDialog(null,
        x, y,
        services, null,  flavor,   attributes);
        if (service != null) try {
            DocPrintJob job = service.createPrintJob();
            String filename = "./tmp.txt";
            FileWriter w = new FileWriter(filename);
            PrintWriter pw = new PrintWriter( w);
            
            generator.printTo(pw);
            pw.close();
            FileInputStream fis = new FileInputStream( filename);
            //            PipedInputStream is = new PipedInputStream();
            //            BufferedInputStream bis = new BufferedInputStream(is);
            //            PipedOutputStream os = new PipedOutputStream();
            //            final PrintStream ps = new PrintStream(os, true);
            //            is.connect(os);
            //            new Thread( new Runnable() {
            //                public void run() {
            //                    ps.println(getLetter());
            //                    ps.close();
            //                }
            //            } ).start();
            SimpleDoc doc = new SimpleDoc( fis , flavor ,null);
            job.print( doc, attributes);
        } catch (Exception e) {
            e.printStackTrace();
            JOptionPane.showInternalMessageDialog(JOptionPane.getDesktopPaneForComponent(this), Globals.bundle.getString("print_error") +": "+ e.toString() );
        }
        
    }//GEN-LAST:event_printButton2ActionPerformed
    
    private void generateLetterButtonActionPerformed(java.awt.event.ActionEvent evt) {//GEN-FIRST:event_generateLetterButtonActionPerformed
        // Add your handling code here:
        try {
            generateReferralFile();
        } catch (Exception e)  {
            e.printStackTrace();
        }
        
        
    }//GEN-LAST:event_generateLetterButtonActionPerformed
    
    
    public org.gnumed.gmIdentity.identity getClient() {
        return client;
    }
    
    public org.gnumed.gmIdentity.identity getProvider() {
        return contacts.getSelectedProvider();
    }
    
    public void setClient(org.gnumed.gmIdentity.identity client) {
        this.client = client;
    }
    
    public void setProvider(org.gnumed.gmIdentity.identity provider) {
        // ? implement
        
    }
    
 
    public void generateReferralFile()  throws Exception {
        generator.setClient(getClient());
        generator.setProvider(getProvider());
        generator.execute();
        jEditorPane1.setText(generator.getLetter());
        jTabbedPane1.setSelectedIndex(1);
    }

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JButton generateLetterButton;
    private javax.swing.JButton jButton1;
    private javax.swing.JEditorPane jEditorPane1;
    private javax.swing.JLabel jLabel1;
    private javax.swing.JPanel jPanel1;
    private javax.swing.JPanel jPanel2;
    private javax.swing.JPanel jPanel3;
    private javax.swing.JPanel jPanel4;
    private javax.swing.JPanel jPanel5;
    private javax.swing.JPanel jPanel6;
    private javax.swing.JScrollPane jScrollPane1;
    private javax.swing.JScrollPane jScrollPane2;
    private javax.swing.JTabbedPane jTabbedPane1;
    private javax.swing.JTextField jTextField1;
    private javax.swing.JButton printButton2;
    private javax.swing.JButton saveButton;
    // End of variables declaration//GEN-END:variables
    
  
}
