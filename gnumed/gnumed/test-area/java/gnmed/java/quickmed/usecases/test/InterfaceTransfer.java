/*
 * InterfaceTransfer.java
 *
 * Created on 9 August 2003, 06:07
 */

package quickmed.usecases.test;
import java.beans.*;

/**
 *
 * @author  sjtan
 */
public class InterfaceTransfer {
    java.util.logging.Logger logger = java.util.logging.Logger.global;
    PropertyDescriptor[] pds;
    String[] excludes;
    Class aInterface;
    final static Object[] zeroArgs = new Object[0];
    /** Creates a new instance of InterfaceTransfer */
    public InterfaceTransfer( Class c, String[] excludes) throws IntrospectionException {
        this.aInterface = c;
        this.excludes = excludes;
        pds = Introspector.getBeanInfo(c).getPropertyDescriptors();
        logger.fine( this + " LOG LEVEL = " + logger.getLevel().getName());
    }
      
    public void transfer( Object from, Object to) throws Exception {
        if ( ! aInterface.isAssignableFrom(from.getClass())
            || ! aInterface.isAssignableFrom(to.getClass()) )
            throw new ClassCastException("MUST BE OF INTERFACE " + aInterface.getName() );
        logger.fine( this + " LOG LEVEL = " + logger.getLevel().getName() + "from="+from + " : to="+to);
        for (int i = 0; i < pds.length; ++i) {
            if (java.util.Arrays.asList(excludes).contains(pds[i].getName()) )
                continue;
            logger.finer("TRANSFERING  " + pds[i].getName() + " FROM " + from.getClass() + " TO " + to.getClass() + " USING WRITE METHOD=" +pds[i].getName());
            try {
            logger.finest("VALUE OF FROM attribute = " +  pds[i].getReadMethod().invoke(from, zeroArgs ) );
            } catch (Exception e) {
                logger.fine(e + " occuring when logging read from " + from);
            }
            if (pds[i].getWriteMethod() == null)
                continue;
            try {
                pds[i].getWriteMethod().invoke(
                to, new Object[] { 
                    pds[i].getReadMethod().invoke(
                    from, zeroArgs ) } );
            } catch (Exception e) {
                e.printStackTrace();
                logger.severe(e.toString() + " from = " + from + "; prop=" + pds[i].getName());
            }
            
        }
    }
    
}
